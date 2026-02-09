import click

@click.command()
@click.pass_obj
def command(context):
    '''
    Reload database and project. This can be used to reload the database when
    package description files have been updated.
    '''

    context.project.save()
    context.project.db.load()
    context.project.load()

# vim: et sts=4 sw=4 ts=4
