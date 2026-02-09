import click

@click.command()
@click.argument('packages', nargs = -1)
@click.pass_obj
def command(context, packages):
    '''
    Dump the dependency graph of a list of packages. If no PACKAGES are
    specified, dump the dependency graph of all selected packages.
    '''

    if len(packages) > 0:
        for name in packages:
            package = context.project.db.find_package(name)
            if not package:
                print('ERROR: package', name, 'not found')
                continue

            package.dump_dependency_graph(context.project.db)
    else:
        for package in context.project.packages:
            package.source.dump_dependency_graph(context.project.db)

# vim: et sts=4 sw=4 ts=4
