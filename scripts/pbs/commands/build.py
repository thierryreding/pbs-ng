description = 'build package(s)'
usage = 'build [options] package [package...]'
summary = ''

def exec(project, *args):
    if len(args) > 1:
        for name in args[1:]:
            package = project.find_package(name)
            if not package:
                print('ERROR: package', name, 'not found')
                continue

            package.build()
    else:
        for package in project.packages:
            package.build()

# vim: et sts=4 sw=4 ts=4
