import click

@click.command()
@click.pass_obj
def command(context):
    '''
    List selected packages.
    '''

    for package in context.project.packages:
        print(package.name)

# vim: et sts=4 sw=4 ts=4
