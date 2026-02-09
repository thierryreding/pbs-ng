import click
import libmount
import pathlib
import tempfile

@click.command()
@click.option('--root', '-r', type = click.Path(path_type = pathlib.Path), default = 'sysroot', help = 'root directory to install packages into')
@click.argument('packages', nargs = -1)
@click.pass_obj
def command(context, root, packages):
    '''
    Install a list of packages. If no PACKAGES are specified, install all
    selected packages.
    '''

    if root.is_file():
        mountpoint = tempfile.TemporaryDirectory()
        target = mountpoint.name

        mnt = libmount.Context()
        mnt.source = root
        mnt.target = target
        mnt.options = 'loop'
        mnt.mount()
    else:
        target = root

    if len(packages):
        for name in packages:
            package = context.project.find_package(name)
            if not package:
                print('ERROR: package', name, 'not found')
                continue

            package.install(target)
    else:
        for package in context.project.packages:
            package.install(target)

    if root.is_file():
        mnt = libmount.Context()
        mnt.target = target
        mnt.umount()

        mountpoint.cleanup()
