import argparse

description = 'configure package(s)'
usage = 'configure [options] package [package...]'
summary = ''

def exec(project, *args):
    parser = argparse.ArgumentParser()
    parser.add_argument('packages', nargs = '*')
    args = parser.parse_args(args[1:])

    if len(args.packages):
        for name in args.packages:
            package = project.find_package(name)
            if not package:
                print('ERROR: package', name, 'not found')
                continue

            package.configure()
    else:
            for package in project.packages:
                package.configure()

# vim: et sts=4 sw=4 ts=4
