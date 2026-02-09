import click

@click.command()
@click.argument('packages', nargs = -1)
@click.pass_obj
def command(context, packages):
    '''
    Select a list of packages.
    '''

    for name in packages:
        print('selecting package', name)
        context.project.select(name)

# vim: et sts=4 sw=4 ts=4
