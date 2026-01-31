description = 'fetch source files'
usage = 'fetch [package...]'
summary = ''

def exec(project, *args):
    if len(args) > 1:
        for name in args[1:]:
            package = project.db.find_package(name)
            package.fetch(keep_going = True)
    else:
        for package in project.packages:
            package.fetch(keep_going = True)
