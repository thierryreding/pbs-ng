import click

@click.command()
@click.argument('packages', nargs = -1)
@click.pass_obj
def command(context, packages):
    '''
    Show package information for a list of packages.
    '''

    for name in packages:
        package = context.project.db.find_package(name)
        if not package:
            print('package "%s" not found' % name)
            continue

        package.dump(0)
