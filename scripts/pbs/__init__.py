import os.path
import sys

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
