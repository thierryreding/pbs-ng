description = 'reload database and project'
usage = 'reload'
summary = ''

def exec(project, *args):
    project.save()
    project.db.load()
    project.load()

# vim: et sts=4 sw=4 ts=4
