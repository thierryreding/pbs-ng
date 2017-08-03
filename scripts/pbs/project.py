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

def error(*args):
    print('\033[1;31mERROR\033[0m:', *args)

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
        def __init__(self, option):
            self.option = option

        def generate_config(self, file = sys.stdout):
            if self.option.default:
                value = 'y'
            else:
                value = 'n'

            print('package.option.%s =' % (self.option.name), value,
                  file = file)

    def __init__(self, project, source):
        self.project = project
        self.source = source
        self.options = []
        self.states = {
            'fetch': None,
            'build': None
        }

        for opt in source.options:
            option = Package.Option(opt)
            self.options.append(option)

    def configure(self):
        print('configuring', self.name)

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

    def fetch(self):
        hash = self.source.hash()

        if self.states['fetch'] != hash or not self.source.exists():
            self.source.fetch()

        self.states['fetch'] = hash

    def filter(self, info):
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

                print(' \033[1;33m*\033[0m creating', filename)

                with tarfile.open(filename, 'w:xz') as tarball:
                    for pattern in package.files:
                        for match in pattern.matches():
                            print('   \033[1;33m-\033[0m %s...' % match,
                                  end = '', flush = True)
                            tarball.add(match,
                                        exclude = pattern.exclude,
                                        filter = self.filter)
                            print('done')

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
            print(' \033[1;32m*\033[0m', self.source.full_name, 'is up-to-date')

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
            print(' \033[1;33m*\033[0m removing %s...' % objtree, end = '',
                  flush = True)
            shutil.rmtree(objtree)
            print('done')

        if not os.path.exists(objtree):
            os.makedirs(objtree)

        self.generate_config(objtree)

        source = os.path.join(pbs.objtree, 'source', pkgtree)
        target = os.path.join(objtree, 'source')

        if not incremental:
            if os.path.exists(source):
                print(' \033[1;33m*\033[0m linking source from %s...' % \
                      os.path.realpath(source), end = '', flush = True)
                os.symlink(source, target)
                print('done')
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

        (columns, lines) = shutil.get_terminal_size()

        wrap = textwrap.TextWrapper(initial_indent = ' \033[1;33m*\033[0m ',
                                    subsequent_indent = ' \033[1;33m>\033[0m ',
                                    break_on_hyphens = False,
                                    width = columns)

        with subprocess.Popen(command, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT) as proc:
            print(' \033[1;33m*\033[0m building %s:' % self.name,
                  ' '.join(command))
            log = io.open(os.path.join(objtree, 'build.log'), 'w')

            while True:
                line = proc.stdout.readline()
                if not line:
                    break

                print(line.decode(), file = log, end = '')
                lines = wrap.wrap(line.decode())

                for line in lines:
                    print(line)

            log.close()

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

        if not distdir:
            parts = self.name.split('/')
            pkgtree = os.path.join('packages', *parts)
            distdir = os.path.join(pbs.objtree, 'dist', pkgtree)

        with pbs.pushd(sysroot):
            if self.source.packages:
                print(' \033[1;33m*\033[0m installing into', os.getcwd())

            for package in self.source.packages:
                filename = '%s-%s.tar.xz' % (package.name, self.version)
                filename = os.path.join(distdir, filename)

                print('   \033[1;33m-\033[0m %s...' % filename, end = '',
                      flush = True)

                filesize = os.path.getsize(filename)

                with io.open(filename, 'rb') as file:
                    with tarfile.open(fileobj = file, mode = 'r') as tarball:
                        for entry in tarball:
                            try:
                                if entry.issym() and os.path.exists(entry.name):
                                    os.unlink(entry.name)

                                tarball.extract(entry)
                            except Exception as e:
                                print('\n     \033[1;31m!\033[0m', e)

                            progress = file.tell() * 100 / filesize
                            print('\r   \033[1;33m-\033[0m %s...%3u%%' %
                                    (filename, progress), end = '',
                                    flush = True)

                print('\r   \033[1;33m-\033[0m %s...done' % filename)

    def load(self, values):
        if not values:
            return

        if 'states' in values:
            for state, value in values['states'].items():
                self.states[state] = value

    def save(self):
        values = {
            'states': {}
        }

        for state in self.states:
            values['states'][state] = self.states[state]

        return values

    def hash(self):
        digest = hashlib.sha1()

        line = 'S %s %s\n' % (self.source.hash(), self.source.full_name)
        digest.update(line.encode())

        for source in self.project.depends.resolve(self.source, direct = True):
            line = 'D %s %s\n' % (source.hash(), source.full_name)
            digest.update(line.encode())

        return digest.hexdigest()

    def watch(self):
        self.source.watch()

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

    def select(self, name, configure = False):
        source = self.db.find_package(name)
        if not source:
            print('package', name, 'not found')
            return None

        for dependency in self.depends.resolve(source, direct = True):
            if not self.select(dependency.full_name):
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
            values['packages'][package.name] = None

        stream = open(filename, 'w')
        yaml.dump(values, stream, default_flow_style = False)
        stream.close()

# vim: et sts=4 sw=4 ts=4
