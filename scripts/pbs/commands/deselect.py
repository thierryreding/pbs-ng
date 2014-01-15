description = 'deselect package'
usage = 'deselect [options] package [package...]'
summary = ''

def exec(project, *args):
    for name in args[1:]:
        print('deselecting package', name)
        project.deselect(name)

# vim: et sts=4 sw=4 ts=4
