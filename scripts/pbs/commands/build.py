import click

@click.command()
@click.option('--force', '-f', is_flag = True, help = 'force package rebuild')
@click.option('--incremental', '-i', is_flag = True, help = 'incremental build (do not rebuild from scratch)')
@click.argument('packages', nargs = -1)
@click.pass_obj
def command(context, force, incremental, packages):
    '''
    Build a list of packages. If no PACKAGES are specified, build all selected
    packages.
    '''

    if len(packages):
        for name in packages:
            package = context.project.find_package(name)
            if not package:
                print('ERROR: package', name, 'not found')
                continue

            package.build(force, incremental)
            context.project.save()
    else:
        for package in context.project.packages:
            package.build(force, incremental)
            context.project.save()

# vim: et sts=4 sw=4 ts=4
