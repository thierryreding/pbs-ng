import argparse
import os.path
import pbs
import shutil
import subprocess

description = 'build initial ramdisk'
usage = 'initrd [options]'
summary = ''

def exec(project, *args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o')
    args = parser.parse_args(args[1:])

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

    if args.output:
        output = args.output
    else:
        output = 'initrd.gz'

    command = [ mkinitrd, '--output', output, sysroot, initrd ]

    pbs.log.info('creating initial ramdisk:', ' '.join(command))

    with subprocess.Popen(command, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT) as proc:
        while True:
            line = proc.stdout.readline()
            if not line:
                break

            line = line.decode()
            pbs.log.quote(line)
