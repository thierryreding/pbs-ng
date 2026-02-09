import click

@click.group(invoke_without_command = True)
@click.pass_context
def command(context):
    '''
    Configure or dump information about the target.
    '''

    if context.invoked_subcommand is None:
        default = context.command.get_command(context, 'show')
        context = default.make_context('show', [], parent = context)
        default.invoke(context)

@command.command()
@click.pass_obj
def show(context):
    context.project.target.dump()

@command.command()
@click.pass_obj
def configure(context):
    context.project.target.configure()
