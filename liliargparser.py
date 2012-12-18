# -*- coding: utf-8 -*-
import sys
import argparse
import constants

class LiliArgParser(object):
    """"""
    
    __argsdict = None
    
    def __init__(self):
        pass
    
    def parse(self):
        parser = argparse.ArgumentParser(prog=constants.__programname__)
        parser.add_argument('-i', nargs='+', help='list of input files')
        parser.add_argument('-w', action='store_true', help='prints a warning when a text line is too long')
        parser.add_argument('-W', action='store_true', help='(EXPERIMENTAL) Attempts at word wrapping text lines')
        parser.add_argument('--version', action='version', version='%(prog)s 2.0')
        args = parser.parse_args(args=sys.argv[1:])
        self._argsdict = vars(args)
        return self
    
    def getinputfiles(self):
        return self._argsdict['i']
    
    def iswarning(self):
        return self._argsdict['w']
    
    def iswordwrap(self):
        return self._argsdict['W']
