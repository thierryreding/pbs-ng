import click

@click.command()
@click.pass_obj
def command(context):
    '''
    Export project configuration. The configuration will be saved to a file
    named `defconfig', which can be used as the starting .config file in a
    new project.
    '''

    context.project.export()

# vim: et sts=4 sw=4 ts=4
