import click

@click.command()
@click.option('--verbose', '-v', is_flag = True, help = 'show verbose messages')
@click.option('--all', '-a', is_flag = True, help = 'scan all packages')
@click.argument('packages', nargs = -1)
@click.pass_obj
def command(context, verbose, all, packages):
    '''
    Scan for new versions of a list of packages. If no PACKAGES are specified,
    scan for new versions of all selected packages.

    If the --all option is specified, scan for new versions of all packages,
    not just selected ones.
    '''

    if all:
        if len(packages):
            print('WARNING: --all is specified, PACKAGES argument ignored')

        for package in context.db.walk():
            package.watch(verbose)
    elif len(packages):
        for name in packages:
            package = context.project.find_package(name)
            if not package:
                print('ERROR: package', name, 'not found')
                continue

            package.watch(verbose)
    else:
        for package in context.project.packages:
            package.watch(verbose)

# vim: et sts=4 sw=4 ts=4
