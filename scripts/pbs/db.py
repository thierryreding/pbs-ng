import hashlib
import http.client
import io
import os, os.path
import pbs
import shutil
import string
import tarfile
import urllib.request
import yaml

def iprint(indent, *args):
    print(' ' * indent, end='')
    print(*args)

class Architecture():
    def __init__(self, name):
        self.name = name

    def parse(self, yaml):
        if 'description' in yaml:
            self.description = yaml['description']
        else:
            self.description = None

    def dump(self, indent):
        iprint(indent, 'Architecture:', self.name)
        iprint(indent, '  Description:', self.description)

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
        src = urllib.request.urlopen(url)

        if isinstance(src, http.client.HTTPResponse):
            headers = dict(src.getheaders())
        else:
            headers = src.info()

        total = int(headers['Content-Length'])
        done = 0

        with open(os.path.join('download', filename), 'wb') as dst:
            while True:
                buf = src.read(512)
                if not buf:
                    break

                done += len(buf)
                dst.write(buf)

                percentage = done * 100 / total

                print("\rDownloading %s... %u%%" % (url, percentage), end = '')

            print()

    def checksum(self):
        basename = self.source.subst(os.path.basename(self.url))
        filename = os.path.join('download', basename)
        digest = hashlib.sha1()

        with open(filename, 'rb') as file:
            while True:
                buf = file.read(512)
                if not buf:
                    break

                digest.update(buf)

            print('digest:', digest.hexdigest())

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
    def __init__(self, section, name):
        self.section = section
        self.name = name

        self.files = []
        self.depends = []
        self.packages = []

    def full_name(self):
        parent = self.section
        name = self.name

        while parent and parent.parent:
            name = parent.name + '/' + name
            parent = parent.parent

        return name

    def parse_source_file(source, yaml):
        for key in yaml.keys():
            if key == 'download':
                source = DownloadSourceFile(source)
                source.parse(yaml[key])
                return source
            else:
                print('ERROR: invalid type of source file:', key)

    def parse(self, yaml):
        if 'description' in yaml:
            self.description = yaml['description']
        else:
            self.description = None

        if 'version' in yaml:
            self.version = str(yaml['version'])
        else:
            self.version = None

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

        for package in self.packages:
            package.dump(indent + 2)

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

        source = Source(section, basename)
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
                parent.add(source)
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

# vim: et sts=4 sw=4 ts=4
