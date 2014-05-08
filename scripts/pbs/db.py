import hashlib
import http.client
import io
import os, os.path
import pbs
import readline
import shutil
import string
import sys
import tarfile
import urllib.request
import yaml

def iprint(indent, *args):
    print(' ' * indent, end='')
    print(*args)

def error(*args):
    print('\033[1;31mERROR\033[0m:', *args)

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
                error('unknown key:', key, 'value:', value)

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
                error('unknown key:', key, 'value:', value)

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
                error('unknown key:', key, 'value:', value)

        for option in self.options:
            if option.default:
                if self.default:
                    error('option', option.name, 'marked as default, but',
                          self.default.name, 'is already the default')
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
                    error('unknown option:', key, 'value:', value)

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

    def dump(self, indent = 0):
        iprint(indent, 'Section:', self.name)

        for section in self.sections:
            section.dump(indent + 2)

        for package in self.packages:
            package.dump(indent + 2)

    def __str__(self):
        return self.name

class Package():
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
                    self.files.append(pattern)

    def dump(self, indent):
        iprint(indent, 'Package:', self.name)
        iprint(indent, '  Description:', self.description)
        iprint(indent, '  Files:')
        for filename in self.files:
            iprint(indent, '   ', filename)

class SourceFile():
    def __init__(self, source):
        self.source = source

    def parse(self, yaml):
        pass

    def fetch(self):
        pass

    def extract(self):
        pass

    def dump(self, indent):
        pass

class DownloadSourceFile(SourceFile):
    def __init__(self, source):
        SourceFile.__init__(self, source)

    def parse(self, yaml):
        SourceFile.parse(self, yaml)

        if 'url' in yaml:
            self.url = yaml['url']
        else:
            self.url = None

        if 'sha1' in yaml:
            self.sha1 = yaml['sha1']
        else:
            self.sha1 = None

    def fetch(self):
        url = self.source.subst(self.url)
        filename = os.path.basename(url)

        filename = os.path.join('download', filename)
        if os.path.exists(filename):
            if self.checksum():
                return

        src = urllib.request.urlopen(url)

        if isinstance(src, http.client.HTTPResponse):
            headers = dict(src.getheaders())
        else:
            headers = src.info()

        if 'Content-Length' in headers:
            total = int(headers['Content-Length'])
        else:
            total = 0

        done = 0

        with open(filename, 'wb') as dst:
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

                print("\r \033[1;33m*\033[0m downloading %s...%s" %
                      (url, progress), end = '')

            print()

    def checksum(self):
        basename = self.source.subst(os.path.basename(self.url))
        filename = os.path.join('download', basename)
        size = os.path.getsize(filename)

        digest = hashlib.sha1()

        with open(filename, 'rb') as file:
            while True:
                buf = file.read(512)
                if not buf:
                    break

                progress = file.tell() * 100 / size

                print('\r \033[1;33m*\033[0m verifying %s...%3u%%' %
                      (filename, progress), end = '')

                digest.update(buf)

            print()

        return digest.hexdigest() == self.sha1

    def extract(self, directory, force = False):
        basename = self.source.subst(os.path.basename(self.url))
        filename = os.path.join('download', basename)

        with io.open(filename, 'rb') as file:
            filesize = file.seek(0, io.SEEK_END)
            file.seek(0, io.SEEK_SET)

            if not os.path.exists(directory):
                os.makedirs(directory)

            with pbs.pushd(directory):
                with tarfile.open(fileobj = file, mode = 'r') as tar:
                    entry = tar.next()
                    if not entry.isdir():
                        print('WARNING: first entry is not a directory')
                        name = os.path.dirname(entry.name)
                    else:
                        name = entry.name

                    if os.path.exists(name) and force:
                        print('removing %s...' % name, end = '', flush = True)
                        shutil.rmtree(name)
                        print('done')

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

                            tar.extract(entry)

                            progress = file.tell() * 100 / filesize
                            print('\r \033[1;33m*\033[0m extracting %s...%3u%%' %
                                    (filename, progress), end = '',
                                    flush = True)

                        status = 'done'
                    else:
                        status = 'skipped'

                    print('\r \033[1;33m*\033[0m extracting %s...%s' %
                            (filename, status))

    def dump(self, indent):
        url = self.source.subst(self.url)
        iprint(indent, 'Download:', url)
        iprint(indent, '  SHA1:', self.sha1)

class Source():
    class Option():
        def __init__(self, name):
            self.name = name
            self.description = None
            self.default = None

        def dump(self, indent):
            iprint(indent, 'Option:', self.name)
            iprint(indent, '  Description:', self.description)
            iprint(indent, '  Default:', self.default)

    def __init__(self, directory, section, name):
        self.directory = directory
        self.section = section
        self.name = name

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

        return super.__getattr__(self, name)

    def parse_source_file(source, yaml):
        for key in yaml.keys():
            if key == 'download':
                source = DownloadSourceFile(source)
                source.parse(yaml[key])
                return source
            else:
                error('invalid type of source file:', key)

    def parse_option(self, name, values):
        option = Source.Option(name)

        if 'description' in values:
            option.description = values['description']

        if 'default' in values:
            option.default = values['default']

        return option

    def parse(self, yaml):
        if 'description' in yaml:
            self.description = yaml['description']
        else:
            self.description = None

        if 'version' in yaml:
            self.version = str(yaml['version'])
        else:
            self.version = None

        if 'depends' in yaml and yaml['depends']:
            for name in yaml['depends']:
                self.depends.append(name)

        if 'options' in yaml and yaml['options']:
            for name in yaml['options']:
                option = Source.parse_option(self, name, yaml['options'][name])
                self.options.append(option)

        if 'files' in yaml:
            for origin in yaml['files']:
                source = Source.parse_source_file(self, origin)
                self.files.append(source)

        if 'packages' in yaml:
            for name in yaml['packages']:
                package = Package(self, name)
                package.parse(yaml['packages'][name])
                self.packages.append(package)

    def subst(self, template):
        keywords = { 'version': self.version }
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

    def dump_dependency_graph(self, stream = sys.stdout):
        if self.depends:
            print('Package', self.name, 'depends on')

            for dependency in self.depends:
                print(' ', dependency, file = stream)

    def fetch(self):
        for source in self.files:
            source.fetch()

    def extract(self, directory):
        for source in self.files:
            source.extract(directory)

    def dump(self, indent):
        iprint(indent, 'Source:', self.name)
        iprint(indent, '  Description:', self.description)

        for source in self.files:
            source.dump(indent + 2)

        for option in self.options:
            option.dump(indent + 2)

        for package in self.packages:
            package.dump(indent + 2)

    def hash(self):
        m = hashlib.sha1()

        for filename in ['package', 'Makefile']:
            m.update(filename.encode())

            filename = os.path.join(self.directory, filename)

            with io.open(filename, 'rb') as file:
                m.update(file.read())

        return m.hexdigest()

class Database():
    def __init__(self):
        pass

    def load_architecture(directory):
        filename = os.path.join(directory, 'architecture')
        basename = os.path.basename(directory)

        stream = open(filename, 'r')
        values = yaml.load(stream)
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
        values = yaml.load(stream)
        stream.close()

        source = Source(directory, section, basename)
        source.parse(values)
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
            directory = os.getcwd()

        self.architectures = Database.load_architectures(directory)
        self.packages = Database.load_packages(directory)

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
                    print(' \033[1;31m!\033[0m no source package found for',
                          dependency)

    def add_section(self, section):
        for subsection in section.sections:
            self.add_section(subsection)

        for package in section.packages:
            self.add_package(package)

    def add_package(self, source):
        node = DependencyGraph.Node(source)
        self.nodes.append(node)

    def resolve(self, node, reverse = True, direct = False):
        if type(node) == str:
            for n in self.nodes:
                if n.source.full_name == node:
                    node = n
        elif type(node) == Source:
            for n in self.nodes:
                if n.source == node:
                    node = n

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
