import distutils.version
import fnmatch
import glob
import hashlib
import http.client
import io
import os, os.path
import pbs
import re
import readline
import shutil
import string
import subprocess
import sys
import tarfile
import urllib.parse
import urllib.request
import yaml
import zipfile

from pbs.version import Version

def iprint(indent, *args):
    print(' ' * indent, end='')
    print(*args)

def resolve_paths(base, component):
    return []

def resolve(scheme, base, component, verbose = False):
    result = []

    # some FTP servers require directory names to end with a /
    if scheme == 'ftp':
        base = base + '/'

    regex = re.compile(component)

    request = urllib.request.urlopen(base)
    for line in request:
        line = line.strip().decode()

        if verbose:
            print(scheme, '>', line)

        if scheme == 'ftp':
            line = line.split(None, 8)[-1]

        match = regex.search(line)
        if match:
            match = match.group(0)

            if match not in result:
                result.append(match)

    return result

class ChecksumError(Exception):
    def __init__(self, source, old, new):
        self.source = source
        self.old = old
        self.new = new

    def __str__(self):
        return '%s: checksum failure for file %s (%s)' % (self.source.source.full_name, self.source.filename, self.new)

class Value():
    def __init__(self, option, value):
        self.option = option
        self.value = value

    def save(self):
        if type(self.value) == Option:
            return { self.option.name: self.value.name }

        if type(self.value) == list:
            values = {}

            for value in self.value:
                values[value.option.name] = value.value

            return { self.option.name: values }

        if self.value:
            return { self.option.name: 'yes' }
        else:
            return { self.option.name: 'no' }

    def dump(self, indent = 0):
        if type(self.value) == Option:
            iprint(indent, '%s: %s' % (self.option.name, self.value.name))
        elif type(self.value) == list:
            iprint(indent, '%s:' % (self.option.name))
            for value in self.value:
                if value.value:
                    status = 'yes'
                else:
                    status = 'no'

                iprint(indent, '  %s: %s' % (value.option.name, status))
        else:
            if value.value:
                status = 'yes'
            else:
                status = 'no'

            iprint(indent, '%s: %s' % (self.option.name, 'yes' if self.value else 'no'))

class Option():
    def __init__(self, name, values):
        self.name = name
        self.default = False
        self.defaults = {}

        for key, value in values.items():
            if key == 'description':
                self.description = value
            elif key == 'default':
                self.default = value
            elif key == 'defaults':
                for key, value in value.items():
                    self.defaults[key] = value
            else:
                pbs.log.error('unknown key:', key, 'value:', value)

    def dump(self, indent = 0):
        if self.default:
            iprint(indent, '* Option:', self.name)
        else:
            iprint(indent, '  Option:', self.name)

        iprint(indent, '    Description:', self.description)

        if self.defaults:
            iprint(indent, '    Defaults:')
            for key, value in self.defaults.items():
                iprint(indent, '      %s: %s' % (key, value))

class OptionGroup():
    def __init__(self, name, values):
        self.name = name
        self.options = []

        for key, value in values.items():
            if key == 'description':
                self.description = value
            elif key == 'options':
                for key, value in value.items():
                    option = Option(key, value)
                    self.options.append(option)
            else:
                pbs.log.error('unknown key:', key, 'value:', value)

    def load(self, values):
        result = []

        for option in self.options:
            if option.name in values:
                value = Value(option, values[option.name])
                result.append(value)

        return [ Value(self, result) ]

    def configure(self, defaults = None):
        result = []

        # make sure defaults is iterable so that the code below can be made
        # more generic
        if defaults is None:
            defaults = []

        print('%s - %s' % (self.name, self.description))

        for option in self.options:
            for default in defaults:
                if default.option == option:
                    default = default.value
                    break
            else:
                default = option.default

            if default:
                yes = 'Y'
                no = 'n'
            else:
                yes = 'y'
                no = 'N'

            while True:
                choice = input('  - %s - %s [%s/%s] ' % (option.name,
                                                         option.description,
                                                         yes, no))
                if choice == 'y' or choice == 'Y':
                    result.append(Value(option, True))
                    break
                elif choice == 'n' or choice == 'N':
                    result.append(Value(option, False))
                    break
                elif not choice:
                    result.append(Value(option, default))
                    break

        return [ Value(self, result) ]

    def dump(self, indent = 0):
        iprint(indent, 'Option group:', self.name)
        iprint(indent, '  Description:', self.description)

        if self.options:
            iprint(indent, '  Options:')
            for option in self.options:
                option.dump(indent + 4)

class Choice():
    def __init__(self, name, values):
        self.name = name
        self.options = []
        self.default = None

        for key, value in values.items():
            if key == 'description':
                self.description = value
            elif key == 'choice':
                for key, value in value.items():
                    option = Option(key, value)
                    self.options.append(option)
            else:
                pbs.log.error('unknown key:', key, 'value:', value)

        for option in self.options:
            if option.default:
                if self.default:
                    pbs.log.error('option', option.name, 'marked as default,'
                                  'but', self.default.name, 'is already the'
                                  'default')
                    option.default = False
                    continue

                self.default = option

    def load(self, value):
        result = []

        for option in self.options:
            if option.name == value:
                value = Value(self, option)
                result.append(value)
                break

        return result

    def configure(self, default = None):
        result = []

        while True:
            num_options = 0
            def_choice = 0
            options = []

            print('%s - %s' % (self.name, self.description))

            for option in self.options:
                prefix = '  '

                if default:
                    if option == default:
                        def_choice = num_options + 1
                        prefix = '* '
                elif option.default:
                    def_choice = num_options + 1
                    prefix = '* '

                print('%s%u. %s - %s' % (prefix, num_options + 1, option.name,
                                         option.description))
                options.append(option)
                num_options += 1

            choice = input('choice[1-%u]: ' % (num_options))

            try:
                if choice:
                    choice = int(choice)
                else:
                    choice = def_choice

                if choice in range(1, num_options + 1):
                    result.append(Value(self, options[choice - 1]))
                    break
            except:
                pass

        return result

    def dump(self, indent = 0):
        iprint(indent, 'Choice:', self.name)
        iprint(indent, '  Description:', self.description)
        iprint(indent, '  Options:');

        indent += 2

        for option in self.options:
            option.dump(indent)

class Architecture():
    def __init__(self, name):
        self.name = name
        self.options = []

    def parse(self, values):
        for key, value in values.items():
            if key == 'description':
                self.description = value
            else:
                if 'options' in value:
                    group = OptionGroup(key, value)
                    self.options.append(group)
                elif 'choice' in value:
                    choice = Choice(key, value)
                    self.options.append(choice)
                else:
                    pbs.log.error('unknown option:', key, 'value:', value)

    def load(self, values):
        for option in self.options:
            if option.name in values:
                print('loading', option.name)
                option.load(values[option.name])

    def dump(self, indent = 0):
        iprint(indent, 'Architecture:', self.name)
        iprint(indent, '  Description:', self.description)

        for option in self.options:
            option.dump(indent + 4)

class Section():
    def __init__(self, parent, name):
        self.parent = parent
        self.sections = []
        self.packages = []
        self.name = name

        if parent:
            parent.sections.append(self)

    def add(self, package):
        self.packages.append(package)

    def find(self, name):
        section = self

        for part in name.split(os.sep)[1:]:
            for section in section.sections:
                if section.name == part:
                    break

        return section

    def walk(self):
        for section in self.sections:
            yield from section.walk()

        for package in self.packages:
            yield package

    def dump(self, indent = 0):
        iprint(indent, 'Section:', self.name)

        for section in self.sections:
            section.dump(indent + 2)

        for package in self.packages:
            package.dump(indent + 2)

    def __str__(self):
        return self.name

class Package():
    class Pattern():
        def __init__(self, source, obj):
            self.source = source
            self.excludes = []

            if type(obj) is dict:
                for pattern, options in obj.items():
                    self.pattern = source.subst(pattern)

                    for option in options:
                        for key, value in option.items():
                            if key == 'exclude':
                                for pattern in value:
                                    self.excludes.append(pattern)
                            else:
                                pbs.log.error('unknown pattern option:', key)
            elif type(obj) is str:
                self.pattern = source.subst(obj)
            else:
                pbs.log.error('unknown pattern type:', obj)
                raise Exception

        def matches(self):
            if self.pattern.startswith(os.sep):
                pattern = self.pattern[len(os.sep):]
            else:
                pattern = self.pattern

            matches = []

            for match in glob.glob(pattern):
                for exclude in self.excludes:
                    if fnmatch.fnmatch(match, exclude):
                        continue

                matches.append(match)

            return matches

        def exclude(self, filename):
            for pattern in self.excludes:
                if fnmatch.fnmatch(filename, pattern):
                    return True

            return False

    def __init__(self, source, name):
        self.source = source
        self.name = name
        self.files = []

    def parse(self, yaml):
        if yaml:
            if 'description' in yaml:
                self.description = yaml['description']
            else:
                self.description = None

            if 'files' in yaml:
                for pattern in yaml['files']:
                    pattern = Package.Pattern(self.source, pattern)
                    self.files.append(pattern)

    def dump(self, indent):
        iprint(indent, 'Package:', self.name)
        iprint(indent, '  Description:', self.description)
        iprint(indent, '  Files:')
        for pattern in self.files:
            iprint(indent, '   ', pattern.pattern)

            if pattern.excludes:
                iprint(indent, '    - exclude:')

                for exclude in pattern.excludes:
                    iprint(indent, '      -', exclude)

class SourceFile():
    def __init__(self, source):
        self.source = source

    def parse(self, yaml):
        pass

    def fetch(self, keep_going = False):
        pass

    def extract(self):
        pass

    def dump(self, indent):
        pass

    def watch(self, verbose = False):
        pass

class DownloadSourceFile(SourceFile):
    def __init__(self, source):
        super().__init__(source)
        self.filename = None
        self.cached = False

    def parse(self, yaml):
        super().parse(yaml)

        if 'url' in yaml:
            self.url = yaml['url']
        else:
            self.url = None

        if 'sha1' in yaml:
            self.sha1 = yaml['sha1']
        else:
            self.sha1 = None

        self.watcher = {
                'url': None
            }

        if 'watch' in yaml and 'url' in yaml['watch']:
            self.watcher['url'] = yaml['watch']['url']

        url = self.source.subst(self.url)
        self.filename = os.path.basename(url)

    def exists(self):
        filename = os.path.join('download', self.filename)

        return os.path.exists(filename)

    def fetch(self, keep_going = False):
        url = self.source.subst(self.url)

        # XXX This is suboptimal because it requires a network connection
        # before it can be determined whether or not the file was already
        # downloaded.
        try:
            headers = {
                'User-Agent': pbs.USER_AGENT
            }

            request = urllib.request.Request(url, headers = headers)
            src = urllib.request.urlopen(request)
        except urllib.error.URLError as e:
            print('failed to open %s:' % url, e)
            return

        if isinstance(src, http.client.HTTPResponse):
            headers = dict(src.getheaders())
        else:
            headers = src.info()

        if 'Content-Disposition' in headers:
            header = headers['Content-Disposition']

            parts = header.split(';')
            if parts[0] == 'attachment':
                if len(parts[1:]) > 1:
                    print('WARNING: attachment:', ';'.join(parts[1:]))

                for part in parts[1:]:
                    key, value = part.strip().split('=')
                    if key == 'filename':
                        self.filename = value
                        self.cached = True
            else:
                print('WARNING: Content-Disposition:', header)

        filename = os.path.join('download', self.filename)
        if os.path.exists(filename):
            src.close()

            old, new = self.checksum()
            if new != old:
                raise ChecksumError(self, old, new)

            return

        pbs.log.begin('downloading %s...' % url)

        if 'Content-Length' in headers:
            total = int(headers['Content-Length'])
        else:
            total = 0

        done = 0

        with open(filename, 'wb') as dst:
            old_progress = -1

            while True:
                buf = src.read(512)
                if not buf:
                    break

                done += len(buf)
                dst.write(buf)

                if total > 0:
                    progress = '%3u%%' % (done * 100 / total)
                else:
                    progress = 'n/a'

                if progress != old_progress:
                    pbs.log.begin('downloading %s...%s' % (url, progress))
                    old_progress = progress

            pbs.log.begin('downloading %s...' % url)
            pbs.log.end('done')

        old, new = self.checksum()
        if new != old:
            raise ChecksumError(self, old, new)

    def checksum(self):
        filename = os.path.join('download', self.filename)
        size = os.path.getsize(filename)

        digest = hashlib.sha1()

        with open(filename, 'rb') as file:
            old_progress = -1

            while True:
                buf = file.read(512)
                if not buf:
                    break

                progress = file.tell() * 100 / size

                if progress != old_progress:
                    pbs.log.begin('verifying %s...%3u%%' % (filename, progress))
                    old_progress = progress

                digest.update(buf)

            pbs.log.begin('verifying %s...' % filename)
            pbs.log.end('done')

        return self.sha1, digest.hexdigest()

    def extract_zip(self, file, filesize):
        with zipfile.ZipFile(file, mode = 'r') as archive:
            old_progress = -1
            first = None

            for info in archive.infolist():
                if not first:
                    name = os.path.dirname(info.filename)

                    if os.path.exists(name) and force:
                        pbs.log.begin('removing %s...' % name)
                        shutil.rmtree(name)
                        pbs.log.end('done')

                    first = info

                parts = info.filename.split(os.sep)
                if len(parts) < 2:
                    continue

                info.filename = os.path.join(*parts[1:])
                archive.extract(info)

                progress = file.tell() * 100 / filesize

                if progress != old_progress:
                    pbs.log.begin('extracting %s...%3u%%' %
                                      (file.name, progress))
                    old_progress = progress

            pbs.log.begin('extracting %s...' % file.name)
            pbs.log.end('done')

    def extract_tar(self, file, filesize):
        with tarfile.open(fileobj = file, mode = 'r') as tar:
            old_progress = -1

            entry = tar.next()
            if not entry.isdir():
                print('WARNING: first entry is not a directory')
                name = os.path.dirname(entry.name)
            else:
                name = entry.name

            if os.path.exists(name) and force:
                pbs.log.begin('removing %s...' % name)
                shutil.rmtree(name)
                pbs.log.end('done')

            if not os.path.exists(name):
                for entry in tar:
                    parts = entry.name.split(os.sep)
                    if len(parts) < 2:
                        continue

                    entry.name = os.path.join(*parts[1:])

                    # rewrite hard- and symlink names
                    if entry.issym() or entry.islnk():
                        link = entry.linkname.split(os.sep)
                        if link[0] == parts[0]:
                            entry.linkname = os.path.join(*link[1:])

                    tar.extract(entry, filter = 'fully_trusted')

                    progress = file.tell() * 100 / filesize

                    if progress != old_progress:
                        pbs.log.begin('extracting %s...%3u%%' %
                                          (file.name, progress))
                        old_progress = progress

                status = 'done'
            else:
                status = 'skipped'

            pbs.log.begin('extracting %s...' % file.name)
            pbs.log.end(status)

    def extract(self, directory, force = False):
        filename = os.path.join('download', self.filename)

        with io.open(filename, 'rb') as file:
            filesize = file.seek(0, io.SEEK_END)
            file.seek(0, io.SEEK_SET)

            if not os.path.exists(directory):
                os.makedirs(directory)

            with pbs.pushd(directory):
                if filename.endswith('.zip'):
                    self.extract_zip(file, filesize)
                else:
                    self.extract_tar(file, filesize)

    def dump(self, indent):
        url = self.source.subst(self.url)
        iprint(indent, 'Download:', url)
        iprint(indent, '  SHA1:', self.sha1)

    def watch(self, verbose = False):
        pbs.log.begin('%s... ' % self.url, indent = 1)

        if self.watcher['url']:
            for watcher in [ pbs.IgnoreWatcher, pbs.AnityaWatcher ]:
                if watcher.match(self.watcher['url']):
                    watcher = watcher(self.watcher['url'], pattern = self.url)
                    break
            else:
                raise Exception('failed to find watcher')
        else:
            watcher = pbs.PackageWatcher.open(self.url)

        results = watcher.watch(verbose = verbose)

        if not results:
            if results is not None:
                pbs.log.error('failed to find any versions')
            else:
                pbs.log.skip('ignored')

            return

        current = Version(self.source.version)
        latest = results[0] # XXX max(results)?

        if latest <= current:
            pbs.log.done('up-to-date')
        else:
            pbs.log.mark('%s' % latest)

class SourceRepository:
    def __init__(self, source, url):
        self.source = source
        self.url = url

    def fetch(self, target):
        pass

class SubversionRepository(SourceRepository):
    def __init__(self, source, url):
        super().__init__(source, url)

    def fetch(self, target):
        pbs.log.begin('checking %s out to %s...' % (self.url, target))

        process = subprocess.run(['svn', 'co', self.url, target],
                                 stderr = subprocess.STDOUT,
                                 stdout = subprocess.PIPE)
        if process.returncode:
            log = process.stdout.decode('utf-8')
            pbs.log.end('failed')
            pbs.log.error(log)
            raise Exception(log)
        else:
            pbs.log.end('done')

    def __str__(self):
        return 'svn: %s' % self.url

class GitRepository(SourceRepository):
    def __init__(self, source, url):
        super().__init__(source, url)

    def fetch(self, target):
        scheme, netloc, path, params, query, fragment, *unused = urllib.parse.urlparse(self.url)

        if fragment:
            branch = [ '--branch', fragment ]
        else:
            branch = []

        url = urllib.parse.urlunparse([scheme, netloc, path, params, query, None, *unused])

        if fragment:
            pbs.log.info('cloning %s (branch %s) to %s...' % (url, fragment, target))
        else:
            pbs.log.info('cloning %s to %s...' % (url, target))

        process = subprocess.run(['git', 'clone', *branch, url, target],
                                 stderr = subprocess.STDOUT,
                                 stdout = subprocess.PIPE)
        if process.returncode:
            log = process.stdout.decode('utf-8')
            pbs.log.end('failed')
            pbs.log.error(log)
            raise Exception(log)
        else:
            pbs.log.end('done')

    def __str__(self):
        return 'git: %s' % self.url

class VCSSourceFile(SourceFile):
    def __init__(self, source):
        super().__init__(source)
        self.repository = None

    def parse(self, yaml):
        super().parse(yaml)

        if 'url' in yaml:
            scheme, netloc, path, *unused = urllib.parse.urlparse(yaml['url'])
            params, query, fragment = unused

            if '+' in scheme:
                system, protocol = scheme.split('+')
            else:
                system = protocol = scheme

            url = urllib.parse.urlunparse([protocol, netloc, path, *unused])

            if system == 'svn':
                self.repository = SubversionRepository(self.source, url)

            if system == 'git':
                self.repository = GitRepository(self.source, url)

            if not self.repository:
                raise Exception('unknown source repository type:', scheme)

            self.url = yaml['url']
        else:
            pbs.log.error('missing URL for source repository:', yaml)

    def exists(self):
        return False

    def extract(self, directory):
        self.repository.fetch(directory)

    def watch(self, verbose = False):
        pbs.log.begin('%s... ' % self.repository, indent = 1)
        pbs.log.skip('skipped')

class Source():
    class Option():
        def __init__(self, name, parent = None):
            self.name = name
            self.parent = parent
            self.description = None
            self.default = None
            self.options = []

        def parse(self, values):
            if 'options' in values and values['options']:
                for name in values['options']:
                    value = values['options'][name]

                    option = Source.parse_option(name, value, self)
                    self.options.append(option)

            if 'default' in values:
                if values['default'] == 'no':
                    self.default = False
                elif values['default'] == 'yes':
                    self.default = True
                else:
                    pbs.log.error('unknown default value', values['default'],
                                  'for option', name)
                    self.default = False
            else:
                pbs.log.error('no default value for option', name)

        def dump(self, indent):
            iprint(indent, 'Option:', self.name)
            iprint(indent, '  Description:', self.description)
            iprint(indent, '  Default:', self.default)

    class Choice():
        class Option():
            def __init__(self, name, values):
                self.name = name
                self.description = None
                self.default = False

        def __init__(self, name, parent = None):
            self.name = name
            self.parent = parent
            self.description = None
            self.default = None
            self.options = []

        def parse(self, values):
            if 'description' in values:
                self.description = values['description']

            for key, value in values['choice'].items():
                option = Option(key, value)
                self.options.append(option)

        def dump(self, indent):
            iprint(indent, 'Choice:', self.name)
            iprint(indent, '  Description:', self.description)

            for option in self.options:
                option.dump(indent + 2)

            iprint(indent, '  Default:', self.default)

    def __init__(self, directory, section, name):
        self.directory = directory
        self.section = section
        self.name = name

        self.description = None
        self.version = ''

        self.files = []
        self.depends = []
        self.options = []
        self.packages = []

    def __getattr__(self, name):
        if name == 'full_name':
            parent = self.section
            name = self.name

            while parent and parent.parent:
                name = parent.name + '/' + name
                parent = parent.parent

            return name

        return super().__getattr__(self, name)

    def parse_source_file(source, yaml):
        for key in yaml.keys():
            if key == 'download':
                source = DownloadSourceFile(source)
                source.parse(yaml[key])
                return source
            elif key == 'source':
                source = VCSSourceFile(source)
                source.parse(yaml[key])
                return source
            else:
                pbs.log.error('invalid type of source file:', key)

    @staticmethod
    def parse_option(name, values, parent = None):
        if 'choice' in values:
            option = Source.Choice(name, parent)
        else:
            option = Source.Option(name, parent)

        if 'description' in values:
            option.description = values['description']

        option.parse(values)
        return option

    def parse(self, values):
        if 'include' in values:
            includes = values['include']

            if isinstance(includes, str):
                includes = [ includes ]

            # includes are relative to the source tree
            for include in includes:
                filename = os.path.join(pbs.srctree, include)

                with open(filename, 'r') as stream:
                    nested = yaml.load(stream, Loader = yaml.BaseLoader)
                    self.parse(nested)

        if 'description' in values:
            self.description = values['description']

        if 'version' in values:
            self.version = str(values['version'])

        if 'depends' in values and values['depends']:
            for name in values['depends']:
                self.depends.append(name)

        if 'options' in values and values['options']:
            for name in values['options']:
                value = values['options'][name]
                option = Source.parse_option(name, value)
                self.options.append(option)

        if 'files' in values:
            for origin in values['files']:
                source = Source.parse_source_file(self, origin)
                self.files.append(source)

        if 'packages' in values:
            for name in values['packages']:
                package = Package(self, name)
                package.parse(values['packages'][name])
                self.packages.append(package)

    def subst(self, template):
        _version = self.version.translate(str.maketrans('.', '_'))

        keywords = {
                'version': self.version,
                'version_': _version,
                '_version': _version,
            }
        version = self.version.split('.')

        if len(version) > 0:
            keywords['major'] = version[0]

        if len(version) > 1:
            keywords['minor'] = version[1]

        if len(version) > 2:
            keywords['micro'] = version[2]

        template = string.Template(template)
        return template.substitute(keywords)

    def __str__(self):
        return self.name

    def dump_dependency_graph(self, db, stream = sys.stdout, depth = 0, chain = []):
        max_depth = 32

        if self.depends:
            if depth > max_depth:
                print('%s  ... %s' % ((' ' * (depth * 2)), ', '.join([x.full_name for x in chain])))
                return

            print('%s%s' % (' ' * (depth * 2), self.full_name), file = stream)

            for dependency in self.depends:
                dependency = db.find_package(dependency)
                circular = dependency in chain

                chain.append(dependency)

                if circular:
                    deps = ', '.join([x.full_name for x in chain])
                    pbs.log.error('circular dependency detected:', deps)
                else:
                    dependency.dump_dependency_graph(db, stream, depth + 1, chain)

                chain.pop()

    def exists(self):
        for source in self.files:
            if not source.exists():
                return False

        return True

    def fetch(self, keep_going = False):
        for source in self.files:
            source.fetch(keep_going = keep_going)

    def extract(self, directory):
        for source in self.files:
            source.extract(directory)

    def dump(self, indent = 0):
        iprint(indent, 'Source:', self.name)
        iprint(indent, '  Description:', self.description)

        for source in self.files:
            source.dump(indent + 2)

        for option in self.options:
            option.dump(indent + 2)

        for package in self.packages:
            package.dump(indent + 2)

    '''
    Obtain the list of a package file's dependencies. This is determined
    by looking at the files that it includes.
    '''
    def includes(self, filename, recursive = True):
        dependencies = []

        with open(filename, 'r') as stream:
            content = yaml.load(stream, Loader = yaml.BaseLoader)

            if 'include' in content:
                includes = content['include']

                if isinstance(includes, str):
                    includes = [ includes ]

                # include files are relative to the source tree
                for include in includes:
                    include = os.path.join(pbs.srctree, include)

                    if recursive:
                        new = self.includes(include)
                        dependencies.extend(new)

                    dependencies.append(include)

        return dependencies

    def hash(self):
        m = hashlib.sha1()

        dependencies = self.includes(os.path.join(self.directory, 'package'))
        dependencies.append(os.path.join(self.directory, 'package'))
        dependencies.append(os.path.join(self.directory, 'Makefile'))

        for filename in dependencies:
            m.update(filename.encode())

            filename = os.path.join(self.directory, filename)

            with io.open(filename, 'rb') as file:
                m.update(file.read())

        return m.hexdigest()

    def watch(self, verbose = False):
        pbs.log.begin('checking %s for updates...' % self.full_name)

        if self.version and self.files:
            print()

            for source in self.files:
                source.watch(verbose)
        else:
            pbs.log.skip('skipped')

class ParseException(Exception):
    def __init__(self, source, message):
        super().__init__('%s: %s' % (source, message))

class Database():
    def __init__(self):
        self.directory = None

    def load_architecture(directory = None):
        if not directory:
            directory = self.directory

        filename = os.path.join(directory, 'architecture')
        basename = os.path.basename(directory)

        stream = open(filename, 'r')
        values = yaml.load(stream, Loader = yaml.BaseLoader)
        stream.close()

        architecture = Architecture(basename)
        architecture.parse(values)
        return architecture

    def load_architectures(directory):
        directory = os.path.join(directory, 'arch')
        architectures = []

        for directory, subdirs, files in os.walk(directory):
            if 'architecture' in files:
                architecture = Database.load_architecture(directory)
                architectures.append(architecture)

        return architectures

    def load_package(section, directory):
        filename = os.path.join(directory, 'package')
        basename = os.path.basename(directory)

        stream = open(filename, 'r')
        values = yaml.load(stream, Loader = yaml.BaseLoader)
        stream.close()

        source = Source(directory, section, basename)

        try:
            source.parse(values)
        except:
            raise ParseException(filename, 'failed to parse')

        return source

    def load_packages(directory):
        packages = os.path.join(directory, 'packages')
        root = None

        for current, subdirs, files in os.walk(packages):
            # find section of current directory
            parent, subdir = os.path.split(os.path.relpath(current, directory))
            if parent:
                if root:
                    parent = root.find(parent)
                    if not parent:
                        parent = root

            # load source package
            if 'package' in files:
                source = Database.load_package(parent, current)
                source.hash()
                parent.add(source)
                # a package is always a leaf, so make sure the tree walk stops
                # here
                del subdirs[:]
                continue

            # if the directory doesn't contain a source package, assume that it
            # contains a section
            section = Section(parent, subdir)
            if not root:
                root = section

        return root

    def load(self, directory = None):
        if not directory:
            if self.directory:
                directory = self.directory
            else:
                directory = os.getcwd()

        self.directory = directory

        self.architectures = Database.load_architectures(directory)
        self.packages = Database.load_packages(directory)

    def walk(self):
        for section in self.packages.sections:
            yield from section.walk()

    def find_package(self, name):
        directory = os.path.dirname(name)
        basename = os.path.basename(name)
        parent = self.packages

        for part in directory.split(os.sep):
            for section in parent.sections:
                if section.name == part:
                    parent = section
                    break

        for package in parent.packages:
            if package.name == basename:
                return package

        return None

    def dump(self, indent):
        iprint(indent, 'Database:')

        for architecture in self.architectures:
            architecture.dump(indent + 2)

        if self.packages:
            self.packages.dump(indent + 2)

class DependencyGraph():
    class Node():
        def __init__(self, source):
            self.source = source
            self.edges = []

        def add_edge(self, node):
            self.edges.append(node)

        def resolve(self):
            print(self.source.full_name)

            for edge in self.edges:
                edge.resolve()

    def __init__(self, db):
        self.nodes = []

        self.add_section(db.packages)

        for node in self.nodes:
            for dependency in node.source.depends:
                for edge in self.nodes:
                    if edge.source.full_name == dependency:
                        node.add_edge(edge)
                        break
                else:
                    pbs.log.error('no source package found for', dependency)

    def add_section(self, section):
        for subsection in section.sections:
            self.add_section(subsection)

        for package in section.packages:
            self.add_package(package)

    def add_package(self, source):
        node = DependencyGraph.Node(source)
        self.nodes.append(node)

    def resolve(self, node, reverse = True, direct = False, chain = []):
        if type(node) == str:
            for n in self.nodes:
                if n.source.full_name == node:
                    node = n
        elif type(node) == Source:
            for n in self.nodes:
                if n.source == node:
                    node = n

        if node in chain:
            graph = ', '.join([x.source.full_name for x in [*chain, node]])
            pbs.log.error('circular dependency detected:', graph)
            return

        chain.append(node)

        if not reverse and not direct:
            yield node.source

        for edge in node.edges:
            if not direct:
                for source in self.resolve(edge):
                    yield source
            else:
                yield edge.source

        if reverse and not direct:
            yield node.source

        chain.pop()

    '''
    Resolve dependency graph and return a list of dependencies in the proper
    order. If reverse is True, then the list will be sorted in reverse order
    (i.e. the node passed in is the last in the list), otherwise the list is
    sorted in forward order (the node passed in is the first in the list).

    The direct parameter can be used to restrict the dependency algorithm to
    the direct dependencies. Direct dependencies are those that the passed
    in node has a direct dependency on. In this mode the node itself will
    not be included in the list of dependencies. By default, the dependency
    graph will be walked fully recursively.
    '''
    def resolve_list(self, node, resolved = [], seen = [], reverse = True, direct = False):
        if type(node) == str:
            for n in self.nodes:
                if n.source.full_name == node:
                    node = n
        elif type(node) == Source:
            for n in self.nodes:
                if n.source == node:
                    node = n

        seen.append(node.source)

        if not reverse and not direct:
            resolved.append(node.source)

        for edge in node.edges:
            if edge.source not in resolved:
                if edge.source in seen:
                    raise Exception('Circular dependency detected: %s -> %s'
                            % (node.source.full_name, edge.source.full_name))

                if not direct:
                    self.resolve_list(edge, resolved, seen, direct = False)
                else:
                    resolved.append(edge.source)

        if reverse and not direct:
            resolved.append(node.source)

        return resolved

    def dump(self):
        for node in self.nodes:
            print('package:', node.source.full_name)
            print('  dependencies:')

            for edge in node.edges:
                print('   ', edge.source.full_name)

# vim: et sts=4 sw=4 ts=4
