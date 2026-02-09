import click

@click.command()
@click.option('--keep-going', '-k', default = True, help = 'Keep going on checksum verification failures.')
@click.argument('packages', nargs = -1)
@click.pass_obj
def command(context, keep_going, packages):
    '''
    Fetch source files for a list of packages. If no PACKAGES are specified,
    fetch the source files for all selected packages.

    The --keep-going option can be specified to continue fetching source files
    even if the checksum verification fails for a package. This is useful when
    downloading all packages in one operation and is the default.
    '''

    if len(packages) > 0:
        for name in packages:
            package = context.project.find_package(name)
            package.fetch(keep_going = keep_going)
    else:
        for package in context.project.packages:
            package.fetch(keep_going = keep_going)
