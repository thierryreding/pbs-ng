description = 'configure target'
usage = 'target [options]'
summary = ''

def exec(project, *args):
    if len(args) > 1:
        subcommand = args[1]
    else:
        subcommand = "show"

    if subcommand == 'configure':
        project.target.configure()
    elif subcommand == 'show':
        project.target.dump()
    else:
        print('%s: subcommand not found' % subcommand)
