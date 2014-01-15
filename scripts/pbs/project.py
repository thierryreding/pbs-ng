import pbs.db
import yaml

class Project():
    def __init__(self, db):
        self.db = db
        self.packages = {}

    def select(self, name):
        self.packages[name] = None

    def deselect(self, name):
        if name in self.packages:
            del self.packages[name]

    def save(self, filename = '.config'):
        values = { 'packages': {} }

        for package in self.packages:
            values['packages'][package] = None

        stream = open(filename, 'w')
        yaml.dump(values, stream, default_flow_style = False)
        stream.close()

    def load(self, filename = '.config'):
        stream = open(filename, 'r')
        values = yaml.load(stream)
        stream.close()

        if 'packages' in values:
            for name in values['packages']:
                self.select(name)

# vim: et sts=4 sw=4 ts=4
