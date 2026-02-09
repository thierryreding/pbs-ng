import click

@click.command()
@click.argument('packages', nargs = -1)
@click.pass_obj
def command(context, packages):
    '''
    Deselect a list of packages.
    '''

    for name in packages:
        print('deselecting package', name)
        context.project.deselect(name)

# vim: et sts=4 sw=4 ts=4
