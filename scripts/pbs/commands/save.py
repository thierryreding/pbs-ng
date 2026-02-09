import click

@click.command()
@click.pass_obj
def command(context):
    '''
    Save project configuration. Many commands do this implicitly, but this
    command is provided as a way of allowing users to manually save, mostly
    to feel good.
    '''

    context.project.save()

# vim: et sts=4 sw=4 ts=4
