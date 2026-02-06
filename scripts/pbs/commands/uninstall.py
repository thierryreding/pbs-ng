import argparse
import libmount
import pathlib
import tempfile

import sys

description = 'uninstall package(s)'
usage = 'uninstall [options] package [package...]'
summary = ''

def exec(project, *args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type = pathlib.Path, help = 'root directory')
    parser.add_argument('packages', nargs = '*')
    args = parser.parse_args(args[1:])

    if args.root:
        path = pathlib.Path(args.root)
    else:
        path = pathlib.Path('sysroot')

    if path.is_file():
        mountpoint = tempfile.TemporaryDirectory()
        target = mountpoint.name

        mnt = libmount.Context()
        mnt.source = args.root
        mnt.target = target
        mnt.options = 'loop'
        mnt.mount()
    else:
        target = path

    if len(args.packages):
        for name in args.packages:
            package = project.find_package(name)
            if not package:
                print('ERROR: package', name, 'not found')
                continue

            package.uninstall(target)
    else:
        for package in project.packages:
            package.uninstall(target)

    if path.is_file():
        mnt = libmount.Context()
        mnt.target = target
        mnt.umount()

        mountpoint.cleanup()
