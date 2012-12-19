# -*- coding: utf-8 -*-
import sys
import argparse
import constants

class LiliArgParser(object):
    """ This class implements the input parser for this program"""
    
    __argsdict = None
    
    def __init__(self):
        pass
    
    def parse(self):
        """ Parse the input arguments """
        parser = argparse.ArgumentParser(prog=constants.__programname__)
        parser.add_argument('-i', nargs='+', help='list of input files')
        parser.add_argument('-f', action='store_true', help='enforces the original text formatting style')
        parser.add_argument('-w', action='store_true', help='prints a warning when a text line is too long')
        parser.add_argument('-W', action='store_true', help='(EXPERIMENTAL) Attempts at word wrapping text lines')
        parser.add_argument('--version', action='version', version='%(prog)s 2.0')
        args = parser.parse_args(args=sys.argv[1:])
        self._argsdict = vars(args)
        return self
    
    def getinputfiles(self):
        return self._argsdict['i']
    
    def istextformat(self):
        """ Returns True if -f was passed, None otherwise """
        return self._argsdict['f']
    
    def iswarning(self):
        return self._argsdict['w']
    
    def iswordwrap(self):
        return self._argsdict['W']
