import functools
import hashlib
import io
import os, os.path
import pbs.db
import readline
import shutil
import subprocess
import sys
import tarfile
import textwrap
import yaml

def iprint(indent, *args):
    print(' ' * indent, end='')
    print(*args)

class BuildError(Exception):
    def __init__(self, package, error):
        self.package = package
        self.error = error

    def __str__(self):
        return 'package %s failed to build: Error %u' % \
                (self.package.full_name, self.error)

class Architecture():
    def __init__(self, source):
        self.source = source
        self.values = []

    def configure(self, project):
        self.project = project
        new = []

        for option in self.source.options:
            default = None

            for value in self.values:
                if value.option == option:
                    default = value.value

            values = option.configure(default)
            new.extend(values)

        self.values = new

    def dump(self, indent = 0):
        iprint(indent, 'Architecture:', self.source.name)

        if self.values:
            iprint(indent, '  Values:');

            for value in self.values:
                value.dump(indent + 4)

    def save(self):
        values = {}

        for value in self.values:
            result = value.save()
            values.update(result)

        return { self.source.name: values }

    def load(self, project, values):
        self.project = project
        self.values = []

        for option in self.source.options:
            for key, value in values.items():
                if key == option.name:
                    result = option.load(value)
                    self.values.extend(result)

    def generate_config(self, file):
        arch = self.source.name

        print('arch = %s' % arch, file = file)

        for value in self.values:
            name = value.option.name

            if type(value.value) is list:
                for option in value.value:
                    if option.value:
                        value = 'y'
                    else:
                        value = 'n'

                    print('arch.%s.%s = %s' % (name, option.option.name, value),
                          file = file)
            else:
                print('arch.%s = %s' % (name, value.value.name), file = file)

        archfile = os.path.join('$(TOP_SRCDIR)', 'arch', arch, 'Makefile')
        print('\ninclude %s' % archfile, file = file)

class Package():
    class Option():
        def __init__(self, option, parent = None):
            self.source = option
            self.parent = parent
            self.value = option.default

            if parent:
                self.name = '%s.%s' % (parent.name, option.name)
            else:
                self.name = option.name

            self.options = Package.parse_options(option.options, self)

        def configure(self, indent = 0):
            source = self.source

            while True:
                yes = 'Y'
                no = 'n'

                if self.value:
                    yes = 'Y'
                    no = 'n'
                else:
                    yes = 'y'
                    no = 'N'

                choice = input('%s%s - %s [%s/%s] ' % (' ' * (indent + 2),
                                                       source.name,
                                                       source.description,
                                                       yes, no))
                if choice == 'y' or choice == 'Y':
                    self.value = True
                    break
                elif choice == 'n' or choice == 'N':
                    self.value = False
                    break
                elif not choice:
                    break

            if self.value:
                for option in self.options:
                    option.configure(indent + 2)

        def generate_config(self, file = sys.stdout):
            if self.value:
                value = 'y'
            else:
                value = 'n'

            print('package.option.%s =' % self.name, value, file = file)

            if self.value:
                for option in self.options:
                    option.generate_config(file = file)

        def load(self, value):
            name = self.source.name

            if value == 'yes':
                self.value = True
            elif value == 'no':
                self.value = False
            else:
                if self.options and isinstance(value, dict):
                    for option in self.options:
                        if option.source.name in value:
                            option.load(value[option.source.name])

                    self.value = True
                else:
                    pbs.log.error('invalid value', value, 'for option', name)

        def save(self):
            values = {}

            if self.value and self.options:
                for option in self.options:
                    if option.value:
                        values[option.source.name] = 'yes'
                    else:
                        values[option.source.name] = 'no'

            if not values:
                values = {
                    self.source.name: 'yes' if self.value else 'no'
                }
            else:
                values = {
                    self.source.name: values
                }

            return values

    class Choice():
        def __init__(self, option, parent = None):
            self.source = option
            self.parent = parent
            self.value = None

        def configure(self):
            while True:
                source = self.source
                num_choices = 0
                choices = []

                print('  %s - %s' % (source.name, source.description))

                for option in source.options:
                    print('    %u. %s - %s' % (num_choices + 1, option.name,
                                               option.description))
                    choices.append(option)
                    num_choices += 1

                choice = input('choice[1-%u]: ' % num_choices)
                option = None

                try:
                    choice = int(choice)
                    if choice in range(1, num_choices + 1):
                        option = choices[choice - 1]
                except:
                    pass

                last = readline.get_current_history_length()
                readline.remove_history_item(last - 1)

                if option:
                    break

            self.value = option

        def generate_config(self, file = sys.stdout):
            name = self.source.name
            value = self.value.name

            print('package.option.%s =' % (name), value, file = file)

        # XXX check that configuration value is a valid choice?
        def load(self, value):
            for option in self.source.options:
                if value == option.name:
                    self.value = option
                    break

        def save(self):
            values = {}

            if self.value:
                values[self.source.name] = self.value.name

            return values

    @staticmethod
    def parse_options(source, parent = None):
        options = []

        for option in source:
            if isinstance(option, pbs.db.Source.Choice):
                option = Package.Choice(option, parent)
            else:
                option = Package.Option(option, parent)

            options.append(option)

        return options

    def __init__(self, project, source):
        self.project = project
        self.source = source
        self.options = []
        self.states = {
            'fetch': None,
            'build': None
        }

        self.options = Package.parse_options(source.options)

    def configure(self):
        if self.options:
            print('configuring %s - %s:' % (self.source.name, self.source.description))

            for option in self.options:
                option.configure()

    def extract(self, directory):
        self.source.extract(directory)

    def generate_config(self, objtree):
        toplevel = os.path.join('$(TOP_OBJDIR)', 'config.mk')
        filename = os.path.join(objtree, 'config.mk')

        with io.open(filename, 'w') as config:
            print('include', toplevel, file = config)
            print(file = config)
            print('package.name =', self.source.name, file = config)
            print('package.version =', self.version, file = config)
            print('', file = config)

            for option in self.options:
                option.generate_config(config)

    def depends(self):
        pass

    def fetch(self, keep_going = False):
        hash = self.source.hash()

        if self.states['fetch'] != hash or not self.source.exists():
            try:
                self.source.fetch()
            except pbs.db.ChecksumError as e:
                if not keep_going:
                    raise e

                hash = None
                print(e)

        if hash:
            self.states['fetch'] = hash

    def filter(self, info, exclude = None):
        if exclude and exclude(info.name):
            return None

        # Default to 0/0 (root/root) as owner and group by default.
        # TODO implement explicit list of permissions to override
        info.uid = 0
        info.gid = 0

        info.uname = 'root'
        info.gname = 'root'

        return info

    def package(self, destdir, distdir):
        if not self.source.packages:
            return

        with pbs.pushd(destdir):
            for package in self.source.packages:
                filename = '%s-%s.tar.xz' % (package.name, self.version)
                filename = os.path.join(distdir, filename)

                pbs.log.info('creating %s' % filename)

                with tarfile.open(filename, 'w:xz') as tarball:
                    for pattern in package.files:
                        for match in pattern.matches():
                            func = functools.partial(self.filter,
                                                     exclude = pattern.exclude)
                            pbs.log.begin('%s...' % match, indent = 1)
                            tarball.add(match, filter = func)
                            pbs.log.end('done')

    def build(self, force = False, incremental = False, dependencies = True, seen = []):
        if dependencies:
            for source in self.project.depends.resolve(self.source, direct = True):
                for package in self.project.packages:
                    if package.source == source:
                        if not package in seen:
                            package.build(False, False, dependencies, seen)
                            seen.append(package)

        hash = self.hash()
        self.fetch()

        if self.states['build'] == hash:
            pbs.log.note('%s is up-to-date' % self.source.full_name)

            if not force:
                return

        parts = self.name.split('/')
        pkgtree = os.path.join('packages', *parts)
        srctree = os.path.join(pbs.srctree, pkgtree)
        objtree = os.path.join(pbs.objtree, pkgtree)
        destdir = os.path.join(pbs.objtree, pkgtree, 'install')
        distdir = os.path.join(pbs.objtree, 'dist', pkgtree)
        sysroot = os.path.join(pbs.objtree, 'sysroot')
        makefile = os.path.join(srctree, 'Makefile')

        if os.path.exists(objtree) and not incremental:
            pbs.log.begin('removing %s...' % objtree)
            shutil.rmtree(objtree)
            pbs.log.end('done')

        if not os.path.exists(objtree):
            os.makedirs(objtree)

        self.generate_config(objtree)

        source = os.path.join(pbs.objtree, 'source', pkgtree)
        target = os.path.join(objtree, 'source')

        if not incremental:
            if os.path.exists(source):
                pbs.log.begin('linking source from %s...' % os.path.realpath(source))
                os.symlink(source, target)
                pbs.log.end('done')
            else:
                target = os.path.join(objtree, 'source')
                self.extract(target)

        command = [ 'make', '--no-print-directory', '-C', objtree,
                    '-f', makefile,
                    'TOP_SRCDIR=%s' % pbs.srctree,
                    'TOP_OBJDIR=%s' % pbs.objtree,
                    'PKGDIR=%s' % pkgtree,
                    'FORCE=%s' % ('y' if incremental else 'n'),
                    'install' ]

        with subprocess.Popen(command, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT) as proc:
            pbs.log.info('building %s:' % self.name, *command)

            with io.open(os.path.join(objtree, 'build.log'), 'w') as log:
                while True:
                    line = proc.stdout.readline()
                    if not line:
                        break

                    line = line.decode()

                    print(line, file = log, end = '')
                    pbs.log.quote(line)

        if proc.returncode != 0:
            raise BuildError(self.source, proc.returncode)

        if not os.path.exists(distdir):
            os.makedirs(distdir)

        self.package(destdir, distdir)
        self.install(sysroot, distdir)

        self.states['build'] = hash

    def install(self, sysroot, distdir = None):
        if not os.path.exists(sysroot):
            os.makedirs(sysroot)

        pkgtree = os.path.join('packages', *self.name.split('/'))

        if not distdir:
            distdir = os.path.join(pbs.objtree, 'dist', pkgtree)

        with pbs.pushd(sysroot):
            if self.source.packages:
                pbs.log.info('installing into %s' % os.getcwd())

            for package in self.source.packages:
                filename = '%s-%s.tar.xz' % (package.name, self.version)
                filename = os.path.join(distdir, filename)

                pbs.log.begin('%s...' % filename, indent = 1)

                filesize = os.path.getsize(filename)

                with io.open(filename, 'rb') as file:
                    with tarfile.open(fileobj = file, mode = 'r') as tarball:
                        for entry in tarball:
                            try:
                                if os.path.exists(entry.name):
                                    if not entry.isdir():
                                        os.remove(entry.name)

                                tarball.extract(entry, filter = 'fully_trusted')
                            except Exception as e:
                                pbs.log.begin('%s...' % filename, indent = 1)
                                pbs.log.fail('failed')
                                raise

                            progress = file.tell() * 100 / filesize
                            pbs.log.begin('%s...%3u%%' % (filename, progress),
                                          indent = 1)

                pbs.log.begin('%s...' % filename, indent = 1)
                pbs.log.end('done')

        filename = os.path.join(pbs.srctree, pkgtree, 'post-install')
        if os.path.exists(filename):
            command = [ filename, sysroot ]

            with subprocess.Popen(command, stdout = subprocess.PIPE,
                                  stderr = subprocess.STDOUT) as proc:
                pbs.log.info('running post-install script for %s...' % (self.name))

                while True:
                    line = proc.stdout.readline()
                    if not line:
                        break

                    line = line.decode()
                    pbs.log.quote(line)

    def load(self, values):
        if not values:
            return

        if 'states' in values:
            for state, value in values['states'].items():
                self.states[state] = value

        # look up cached filename
        if 'files' in values:
            for url, filename in values['files'].items():
                for source in self.source.files:
                    if source.url == url and source.filename != filename:
                        source.filename = filename
                        source.cached = True

        if self.options and 'options' in values:
            values = values['options']

            for option in self.options:
                name = option.source.name
                # XXX enforce that we need a valid value here? force package
                #     configuration if there is none?
                if name in values:
                    option.load(values[name])
                else:
                    option.load(None)

    def save(self):
        values = {
            'states': {}
        }

        for state in self.states:
            values['states'][state] = self.states[state]

        if self.options:
            values['options'] = {}

            for option in self.options:
                values['options'].update(option.save())

        if self.source.files:
            for source in self.source.files:
                if isinstance(source, pbs.db.DownloadSourceFile):
                    if source.cached:
                        if 'files' not in values:
                            values['files'] = {}

                        values['files'][source.url] = source.filename

        return values

    def hash(self):
        digest = hashlib.sha1()

        line = 'S %s %s\n' % (self.source.hash(), self.source.full_name)
        digest.update(line.encode())

        for source in self.project.depends.resolve(self.source, direct = True):
            line = 'D %s %s\n' % (source.hash(), source.full_name)
            digest.update(line.encode())

        return digest.hexdigest()

    def watch(self, verbose = False):
        self.source.watch(verbose)

    def get_version(self):
        pkgtree = os.path.join('packages', *self.name.split('/'))
        srctree = os.path.join(pbs.srctree, pkgtree)
        objtree = os.path.join(pbs.objtree, pkgtree)
        makefile = os.path.join(srctree, 'Makefile')
        command = [ 'make', '--no-print-directory', '-C', objtree,
                    '-f', makefile,
                    'TOP_SRCDIR=%s' % pbs.srctree,
                    'TOP_OBJDIR=%s' % pbs.objtree,
                    'PKGDIR=%s' % pkgtree,
                    'version' ]

        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
            return proc.stdout.readline().decode('utf-8').strip()

        return None

    def __getattr__(self, name):
        if name == 'name':
            return self.source.full_name

        if name == 'version':
            if self.source.version:
                return self.source.version

            return self.get_version()

        return super.__getattr__(self, name)

class Target():
    def __init__(self, project):
        self.project = project
        self.architecture = None

    def configure(self):
        while True:
            num_choices = 0
            choices = []

            for architecture in self.project.db.architectures:
                print('  %u. %s - %s' % (num_choices + 1, architecture.name,
                                         architecture.description))
                choices.append(architecture)
                num_choices += 1

            choice = input('choice[1-%u]: ' % num_choices)
            architecture = None

            try:
                choice = int(choice)
                if choice in range(1, num_choices + 1):
                    architecture = choices[choice - 1]
            except:
                pass

            last = readline.get_current_history_length()
            readline.remove_history_item(last - 1)

            if architecture:
                break

        if not self.architecture:
            self.architecture = Architecture(architecture)

        self.architecture.configure(self.project)
        self.generate_config()

    def save(self):
        values = {
            'architecture': {}
        }

        values['architecture'] = self.architecture.save()

        return values

    def load(self, values):
        if 'architecture' in values:
            for key, value in values['architecture'].items():
                for architecture in self.project.db.architectures:
                    if key == architecture.name:
                        self.architecture = Architecture(architecture)
                        self.architecture.load(self.project, value)
                        break

                break

        self.generate_config()

    def dump(self, indent = 0):
        iprint(indent, 'Target:')
        if self.architecture:
            self.architecture.dump(indent + 2)

    def generate_config(self):
        with io.open('target.mk', 'w') as file:
            self.architecture.generate_config(file)

class Project():
    def __init__(self, db):
        self.db = db
        self.target = Target(self)
        self.packages = []

    def setup(self):
        if not os.path.exists('target.mk'):
            print("Target is not configured, please run `target configure'")

        if not os.path.exists('config.mk'):
            print("generating `config.mk'...")

            toplevel = os.path.join('$(TOP_SRCDIR)', 'config.mk')
            target = os.path.join('$(TOP_OBJDIR)', 'target.mk')

            with io.open('config.mk', 'w') as file:
                print('include', toplevel, file = file)
                print('include', target, file = file)

        if not os.path.exists('download'):
            if os.path.lexists('download'):
                print("removing dangling symlink `download'")
                os.unlink('download')

            relpath = os.path.relpath(pbs.srctree, pbs.objtree)
            directory = os.path.join(relpath, 'download')

            print("symlinking `download' to `%s'..." % directory)
            os.symlink(directory, 'download')

    def find_package(self, name):
        source = self.db.find_package(name)

        for package in self.packages:
            if package.source == source:
                return package

        return None

    def select(self, name, configure = False, stack = []):
        source = self.db.find_package(name)
        if not source:
            print('package', name, 'not found')
            return None

        for dependency in self.depends.resolve(source, direct = True):
            if not self.select(dependency.full_name, configure, stack):
                print('package %s depends on non-existent package %s' %
                        (name, dependency.full_name))

        for package in self.packages:
            if package.source == source:
                return package

        package = Package(self, source)

        if configure:
            package.configure()

        self.packages.append(package)
        return package

    def deselect(self, name):
        source = self.db.find_package(name)
        if not source:
            print('package', name, 'not found')
            return

        for package in self.packages:
            if package.source == source:
                self.packages.remove(package)

    def save(self, filename = '.config'):
        values = {
            'target': {},
            'packages': {}
        }

        values['target'] = self.target.save()

        for package in self.packages:
            values['packages'][package.name] = package.save()

        stream = open(filename, 'w')
        yaml.dump(values, stream, default_flow_style = False)
        stream.close()

    def load(self, filename = '.config'):
        # reset state
        self.depends = pbs.db.DependencyGraph(self.db)
        del self.packages[:]

        try:
            with open(filename, 'r') as stream:
                values = yaml.load(stream, Loader = yaml.loader.BaseLoader)
        except:
            return

        if 'target' in values:
            self.target.load(values['target'])

        if 'packages' in values:
            for name in values['packages']:
                package = self.select(name)
                if package:
                    package.load(values['packages'][name])

        self.setup()

    def export(self, filename = 'defconfig'):
        values = {
            'packages': {}
        }

        values['target'] = self.target.save()

        for package in self.packages:
            values['packages'][package.name] = {}

            if package.options:
                options = values['packages'][package.name]['options'] = {}

                for option in package.options:
                    options.update(option.save())

        stream = open(filename, 'w')
        yaml.dump(values, stream, default_flow_style = False)
        stream.close()

# vim: et sts=4 sw=4 ts=4
