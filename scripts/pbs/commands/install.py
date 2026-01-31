import argparse
import libmount
import pathlib
import tempfile

import sys

description = 'install package(s)'
usage = 'install [options] package [package...]'
summary = ''

def exec(project, *args):
    parser = argparse.ArgumentParser()
    parser.add_argument('root')
    parser.add_argument('packages', nargs = '*')
    args = parser.parse_args(args[1:])

    path = pathlib.Path(args.root)

    if path.is_file():
        mountpoint = tempfile.TemporaryDirectory()
        target = mountpoint.name

        mnt = libmount.Context()
        mnt.source = args.root
        mnt.target = target
        mnt.options = 'loop'
        mnt.mount()
    else:
        target = args.root

    if len(args.packages):
        for name in args.packages:
            package = project.find_package(name)
            if not package:
                print('ERROR: package', name, 'not found')
                continue

            package.install(target)
    else:
        for package in project.packages:
            package.install(target)

    if path.is_file():
        mnt = libmount.Context()
        mnt.target = target
        mnt.umount()

        mountpoint.cleanup()
