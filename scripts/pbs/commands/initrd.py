import click
import os.path
import pbs
import shutil
import subprocess

@click.command()
@click.option('--output', '-o', type = click.Path(), default = 'initrd.gz', help = 'output filename of the initial ramdisk')
@click.pass_obj
def command(context, output):
    '''
    Build an initial ramdisk. This uses an existing sysroot as the source for
    files to be copied.
    '''

    sysroot = os.path.join(pbs.objtree, 'sysroot')
    initrd = os.path.join(pbs.objtree, 'initrd')
    mkinitrd = os.path.join(sysroot, 'usr/bin/mkinitrd')

    if not os.path.exists(mkinitrd):
        pbs.log.error('%s not found' % mkinitrd)
        return

    if os.path.exists(initrd):
        pbs.log.begin('removing %s...' % initrd)
        shutil.rmtree(initrd)
        pbs.log.end('done')

    cmd = [ mkinitrd, '--output', output, sysroot, initrd ]

    pbs.log.info('creating initial ramdisk:', ' '.join(cmd))

    with subprocess.Popen(cmd, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT) as proc:
        while True:
            line = proc.stdout.readline()
            if not line:
                break

            line = line.decode()
            pbs.log.quote(line)
