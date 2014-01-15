description = 'list selected packages'
usage = 'list'
summary = ''

def exec(project, *args):
    for package in project.packages:
        print('package:', package)

# vim: et sts=4 sw=4 ts=4
