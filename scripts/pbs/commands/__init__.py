from importlib.machinery import PathFinder
import os.path

def load(directory):
    curdir = os.path.join(directory, 'scripts', 'pbs', 'commands')
    commands = {}

    for dir, subdirs, files in os.walk(curdir):
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext == '.py' and name != '__init__':
                loader = PathFinder.find_module(name, [curdir])
                commands[name] = loader.load_module()

    return commands
