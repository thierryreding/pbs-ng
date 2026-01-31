description = 'dump dependency graph'
usage = 'depends [options] package [package...]'
summary = ''

def exec(project, *args):
    if len(args) > 1:
        for name in args[1:]:
            package = project.db.find_package(name)
            if not package:
                print('ERROR: package', name, 'not found')
                continue

            package.dump_dependency_graph(project.db)
    else:
        for package in project.packages:
            package.source.dump_dependency_graph(project.db)

# vim: et sts=4 sw=4 ts=4
