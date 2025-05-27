import os.path
import shutil
import sys
import textwrap

VERSION = '2025.05'

import pbs.watch

PackageWatcher = pbs.watch.PackageWatcher
IndexWatcher = pbs.watch.IndexWatcher

srctree = os.path.realpath(os.path.dirname(sys.argv[0]))
objtree = os.getcwd()

'''
os.chdir() context manager
'''
class pushd(object):
    def __init__(self, directory):
        self.new = directory

    def __enter__(self):
        self.old = os.getcwd()
        os.chdir(self.new)

    def __exit__(self, type, value, trace):
        os.chdir(self.old)

class Logger():
    colors = {
        'black': '30',
        'red': '31',
        'green': '32',
        'yellow': '33',
        'blue': '34',
        'magenta': '35',
        'cyan': '36',
        'white': '37',
    }

    indents = {
        'error': {
            'prefix': '!',
            'cont': '>',
            'color': '31',
        },
        'note': {
            'prefix': '*',
            'cont': '>',
            'color': '32',
        },
        'info': {
            'prefix': '*-',
            'cont': '>',
            'color': '33',
        },
        'quote': {
            'prefix': '|',
            'cont': '>',
            'color': '34',
        },
    }

    @staticmethod
    def create_indents(level, color = False, index = 0):
        indent = Logger.indents[level]
        prefix = ' ' * (index * 2)

        if color:
            init = ' %s\033[%s;1m%s\033[0m ' % (prefix, indent['color'],
                                                indent['prefix'][index])
            subs = ' %s\033[%s;1m%s\033[0m ' % (prefix, indent['color'],
                                                indent['cont'])
        else:
            init = ' %s%s ' % (prefix, indent['prefix'][index])
            subs = ' %s%s ' % (prefix, indent['cont'])

        return (init, subs)

    @staticmethod
    def create_wrapper(level, columns, color = False, continuation = False,
                       index = 0):
        (init, subs) = Logger.create_indents(level, color, index)

        if continuation:
            init = ' ' * (index * 2)

        return textwrap.TextWrapper(initial_indent = init,
                                    subsequent_indent = subs,
                                    break_on_hyphens = False,
                                    width = columns)

    @staticmethod
    def concat(*args):
        return ' '.join([str(a) for a in args])

    @staticmethod
    def wrap(wrapper, *args):
        message = Logger.concat(*args)
        return wrapper.wrap(message)

    def __init__(self, color = False):
        self.color = color

        (columns, lines) = shutil.get_terminal_size()

        self.note_wrap = Logger.create_wrapper('note', columns, color, False)

        self.info_wrap = []
        self.info_cont = []

        for i in range(0, 2):
            wrap = Logger.create_wrapper('info', columns, color, False, i)
            cont = Logger.create_wrapper('info', columns, color, True, i)

            self.info_wrap.append(wrap)
            self.info_cont.append(cont)

        self.error_wrap = Logger.create_wrapper('error', columns, color, False)
        self.quote_wrap = Logger.create_wrapper('quote', columns, color, False)

    def colorize(self, color, bold, *args):
        message = Logger.concat(*args)

        if self.color and color:
            if bold:
                flags = 1
            else:
                flags = 0

            message = '\033[%s;%sm%s\033[0m' % (Logger.colors[color], flags,
                                                message)

        return message

    def begin(self, *args, indent = 0):
        lines = Logger.wrap(self.info_wrap[indent], *args)
        last = lines.pop()

        for line in lines:
            print(line)

        print('\r%s' % last, end = '', flush = True)

    def end(self, *args, color = None, indent = 0):
        text = self.colorize(color, True, *args)

        lines = Logger.wrap(self.info_cont[indent], *args)
        for line in lines:
            print(line)

    def mark(self, *args):
        text = self.colorize('yellow', True, *args)

        lines = Logger.wrap(self.info_cont[0], text)
        for line in lines:
            print(line)

    def skip(self, *args):
        text = self.colorize('magenta', True, *args)

        lines = Logger.wrap(self.info_cont[0], text)
        for line in lines:
            print(line)

    def fail(self, *args):
        text = self.colorize('red', True, *args)

        lines = Logger.wrap(self.info_cont[0], text)
        for line in lines:
            print(line)

    def done(self, *args):
        text = self.colorize('green', True, *args)

        lines = Logger.wrap(self.info_cont[0], text)
        for line in lines:
            print(line)

    def note(self, *args):
        lines = Logger.wrap(self.note_wrap, *args)
        for line in lines:
            print(line)

    def info(self, *args, indent = 0):
        lines = Logger.wrap(self.info_wrap[indent], *args)
        for line in lines:
            print(line)

    def error(self, *args):
        lines = Logger.wrap(self.error_wrap, *args)
        for line in lines:
            print(line)

    def quote(self, *args):
        lines = Logger.wrap(self.quote_wrap, *args)
        for line in lines:
            print(line)

log = Logger(color = True)
