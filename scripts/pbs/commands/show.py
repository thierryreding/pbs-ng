description = 'show package information'
usage = 'show package [package...]'
summary = ''

def exec(project, *args):
    if len(args) < 2:
        print('usage: %s' % usage)
        return

    for name in args[1:]:
        package = project.db.find_package(name)
        if not package:
            print('package "%s" not found' % name)
            continue

        package.dump(0)
