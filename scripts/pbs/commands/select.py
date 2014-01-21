description = 'select package(s)'
usage = 'select [options] package [package...]'
summary = ''

def exec(project, *args):
    for name in args[1:]:
        print('selecting package', name)
        project.select(name)

# vim: et sts=4 sw=4 ts=4
