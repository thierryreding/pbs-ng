import click

@click.command()
@click.argument('packages', nargs = -1)
@click.pass_obj
def command(context, packages):
    '''
    Configure a list of packages. If no PACKAGES are specified, configure all
    selected packages.
    '''

    if len(packages):
        for name in packages:
            package = context.project.find_package(name)
            if not package:
                print('ERROR: package', name, 'not found')
                continue

            package.configure()
    else:
            for package in context.project.packages:
                package.configure()

# vim: et sts=4 sw=4 ts=4
