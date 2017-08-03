import argparse

description = 'build package(s)'
usage = 'build [options] package [package...]'
summary = ''

def exec(project, *args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--force', '-f', action = 'store_true')
    parser.add_argument('--incremental', '-i', action = 'store_true')
    parser.add_argument('packages', nargs = '*')
    args = parser.parse_args(args[1:])

    if len(args.packages):
        for name in args.packages:
            package = project.find_package(name)
            if not package:
                print('ERROR: package', name, 'not found')
                continue

            package.build(args.force, args.incremental)
    else:
        for package in project.packages:
            package.build(args.force, args.incremental)

# vim: et sts=4 sw=4 ts=4
