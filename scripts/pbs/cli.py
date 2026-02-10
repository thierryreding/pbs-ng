import click, cmd, importlib, os.path, readline, shlex, time
import pbs, pbs.db, pbs.project

PATH = os.path.join(os.path.dirname(__file__), 'commands')

class RuntimeGroup(click.Group):
    def __init__(self, *args, path = PATH, **kwargs):
        super().__init__(*args, **kwargs)
        self.runtime = {}

        if path:
            for entry in os.scandir(path):
                name, ext = os.path.splitext(entry.name)
                if ext == '.py' and name != '__init__':
                    spec = importlib.machinery.PathFinder.find_spec(name, [path])
                    self.runtime[name] = spec.loader.load_module()

    def list_commands(self, ctx):
        base = super().list_commands(ctx)
        runtime = sorted(self.runtime.keys())
        return base + runtime

    def get_command(self, ctx, name):
        if name not in self.runtime:
            cmd = super().get_command(ctx, name)
        else:
            cmd = self.runtime[name].command

        return cmd

class ContextObject:
    def __init__(self):
        self.db = pbs.db.Database()
        start = time.perf_counter()
        self.db.load(pbs.srctree)
        end = time.perf_counter()
        print('loaded database in %f seconds' % (end - start))

        self.project = pbs.project.Project(self.db)
        self.project.load()

        print('source directory:', pbs.srctree)
        print('output directory:', pbs.objtree)

class REPLContext(click.Context):
    def fail(self, message: str):
        option = self.help_option_names[0]
        command = self.command_path

        click.echo(self.get_usage())
        click.echo('')
        click.echo(f"Try '{command} {option}' for help")
        click.echo('')
        click.echo(message)

        super().fail(message)

    def exit(self, code: int = 0):
        super().exit(code)

class REPL(cmd.Cmd):
    prompt = '> '

    def __init__(self, context):
        super().__init__(self)
        self.context = context

    def preloop(self):
        if os.path.exists('.history'):
            readline.read_history_file('.history')

    def postloop(self):
        readline.write_history_file('.history')

    def do_help(self, arg):
        cli = self.context.command

        if arg:
            command = cli.get_command(self.context, arg)
            if command:
                context = command.make_context(arg, [], parent = self.context)
                usage = command.get_help(context)
            else:
                usage = cli.get_help(self.context)
        else:
            usage = cli.get_help(self.context)

        click.echo(usage)

    def default(self, line):
        if line == 'EOF':
            return True

        cli = self.context.command
        args = shlex.split(line)
        command = cli.get_command(self.context, args[0])
        if not command:
            print(cli.get_help(self.context))
        else:
            try:
                context = command.make_context(args[0], args[1:], parent = self.context)
                result = command.invoke(context)
            except click.exceptions.Exit as e:
                pass
            except click.exceptions.NoSuchOption as e:
                click.echo(e.message)
            except click.exceptions.UsageError as e:
                pass
            except KeyboardInterrupt:
                print('')
            except Exception as e:
                pbs.log.error(e)

        return False

@click.group(cls = RuntimeGroup, help = 'Platform Build System CLI', invoke_without_command = True)
@click.pass_context
def CLI(context):
    if context.invoked_subcommand is None:
        pbs.log.startup = False
        pbs.isolate()

        click.BaseCommand.context_class = REPLContext
        repl = REPL(context)
        repl.cmdloop()
        print()
