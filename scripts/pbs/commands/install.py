import argparse

description = 'install package(s)'
usage = 'install [options] package [package...]'
summary = ''

def exec(project, *args):
    parser = argparse.ArgumentParser()
    parser.add_argument('root')
    parser.add_argument('packages', nargs = '*')
    args = parser.parse_args(args[1:])

    if len(args.packages):
        for name in args.packages:
            package = project.find_package(name)
            if not package:
                print('ERROR: package', name, 'not found')
                continue

            package.install(args.root)
    else:
        for package in project.packages:
            package.install(args.root)
