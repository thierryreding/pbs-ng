import glob
import io
import os, os.path
import pbs.db
import subprocess
import tarfile
import yaml

class Package():
    def __init__(self, source):
        self.source = source

    def configure(self):
        print('configuring', self.name)

    def extract(self, directory):
        self.source.extract(directory)

    def generate_config(self, objtree):
        relpath = os.path.relpath(pbs.objtree, objtree)
        toplevel = os.path.join(relpath, 'config.mk')
        filename = os.path.join(objtree, 'config.mk')

        with open(filename, 'w') as config:
            print('include', toplevel, file = config)
            print(file = config)
            print('PACKAGE =', self.source.name, file = config)
            print('VERSION =', self.source.version, file = config)

    def package(self, destdir, distdir):
        with pbs.pushd(destdir):
            for package in self.source.packages:
                filename = '%s-%s.tar.xz' % (package.name, self.source.version)
                filename = os.path.join(distdir, filename)

                print(' \033[1;33m*\033[0m creating', filename)

                with tarfile.open(filename, 'w:xz') as tarball:
                    for pattern in package.files:
                        if pattern.startswith(os.sep):
                            pattern = pattern[len(os.sep):]

                        for match in glob.glob(pattern):
                            print('   \033[1;33m-\033[0m %s...' % match,
                                  end = '', flush = True)
                            tarball.add(match)
                            print('done')

    def build(self):
        parts = self.name.split('/')
        pkgtree = os.path.join('packages', *parts)
        srctree = os.path.join(pbs.srctree, pkgtree)
        objtree = os.path.join(pbs.objtree, pkgtree)
        destdir = os.path.join(pbs.objtree, pkgtree, 'install')
        distdir = os.path.join(pbs.objtree, 'dist', pkgtree)
        sysroot = os.path.join(pbs.objtree, 'sysroot')
        makefile = os.path.join(srctree, 'Makefile')

        if not os.path.exists(objtree):
            os.makedirs(objtree)

        self.generate_config(objtree)
        self.extract(objtree)

        command = [ 'make', '--no-print-directory', '-C', objtree,
                    '-f', makefile,
                    'TOP_SRCDIR=%s' % pbs.srctree,
                    'TOP_OBJDIR=%s' % pbs.objtree,
                    'PKGDIR=%s' % pkgtree,
                    'install' ]

        with subprocess.Popen(command, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT) as proc:
            print(' \033[1;33m*\033[0m building %s:' % self.name,
                  ' '.join(command))

            while True:
                line = proc.stdout.readline()
                if not line:
                    break

                print(' \033[1;32m|\033[0m', *line.decode().splitlines())

        print('process finished with', proc.returncode)

        if not os.path.exists(distdir):
            os.makedirs(distdir)

        self.package(destdir, distdir)
        self.install(distdir, sysroot)

    def install(self, distdir, sysroot):
        if not os.path.exists(sysroot):
            os.makedirs(sysroot)

        with pbs.pushd(sysroot):
            print(' \033[1;33m*\033[0m installing into', os.getcwd())

            for package in self.source.packages:
                filename = '%s-%s.tar.xz' % (package.name, self.source.version)
                filename = os.path.join(distdir, filename)

                print('   \033[1;33m-\033[0m %s...' % filename, end = '',
                      flush = True)

                with io.open(filename, 'rb') as file:
                    filesize = file.seek(0, io.SEEK_END)
                    file.seek(0, io.SEEK_SET)

                    with tarfile.open(fileobj = file, mode = 'r') as tarball:
                        for entry in tarball:
                            tarball.extract(entry)

                            progress = file.tell() * 100 / filesize
                            print('\r   \033[1;33m-\033[0m %s...%3u%%' %
                                    (filename, progress), end = '',
                                    flush = True)

                print('\r   \033[1;33m-\033[0m %s...done' % filename)

    def __getattr__(self, name):
        if name == 'name':
            return self.source.full_name()

        return super.__getattr__(self, name)

class Project():
    def __init__(self, db):
        self.db = db
        self.packages = []

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
            return False

        package = Package(source)

        if configure:
            package.configure()

        self.packages.append(package)

    def deselect(self, name):
        if name in self.packages:
            del self.packages[name]

    def save(self, filename = '.config'):
        values = { 'packages': {} }

        for package in self.packages:
            values['packages'][package.name] = None

        stream = open(filename, 'w')
        yaml.dump(values, stream, default_flow_style = False)
        stream.close()

    def load(self, filename = '.config'):
        try:
            with open(filename, 'r') as stream:
                values = yaml.load(stream)
        except:
            return

        if 'packages' in values:
            for name in values['packages']:
                self.select(name)

# vim: et sts=4 sw=4 ts=4
