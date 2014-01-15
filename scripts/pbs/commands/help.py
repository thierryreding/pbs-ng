import os.path
import sys

import pbs.commands

srctree = os.path.realpath(os.path.dirname(sys.argv[0]))

description = 'display help information'
usage = 'help [command]'
summary = ''

def exec(project, *args):
    commands = pbs.commands.load(srctree)
    name_len = 0

    if len(args) > 2:
        print('usage: %s' % usage)
        return

    if len(args) < 2:
        print('Available commands:')

        for name in sorted(commands.keys()):
            if len(name) > name_len:
                name_len = len(name)

        for name, command in sorted(commands.items()):
            if hasattr(command, 'description'):
                description = command.description
            else:
                description = ''

            print('  %-*s - %s' % (name_len, name, description))
    else:
        if args[1] not in commands:
            print('unknown command "%s"' % args[1])
            return

        command = commands[args[1]]

        print('Usage: %s' % command.usage)
        print()
        print('Synopsis: %s' % command.description)
        print()
        print(summary)
