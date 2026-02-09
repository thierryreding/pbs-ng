import click

@click.command()
@click.pass_obj
def command(context):
    '''
    Exit interactive shell.
    '''

    raise EOFError
