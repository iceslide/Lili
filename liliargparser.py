# -*- coding: utf-8 -*-
import sys
import argparse

import constants

__author__ = constants.__author__
__copyright__ = constants.__copyright__
__license__  = constants.__license__

class LiliArgParser(object):
    """ This class implements the input parser for this program"""
    
    __argsdict = None
    
    def __init__(self):
        pass
    
    def parse(self, arglist=None):
        """ Parse the input arguments """
        parser = argparse.ArgumentParser(prog=constants.__appname__)
        parser.add_argument('-e', 
            help='specify the input file encoding. Default: Shift-jis')
        parser.add_argument('-i', type=str, action="store", help='input file')
        parser.add_argument('-f', action='store_true',
            help='format the file following Lilith\'s style guidelines')
        parser.add_argument('-o', type=str, help='output file')
        parser.add_argument('-t', action='store_true',
            help='output only the game text')
        parser.add_argument('-w', action='store_true',
            help='prints a warning when a text line is too long')
        parser.add_argument('-W', action='store_true',
            help='(EXPERIMENTAL) Basic word wrapping')
        parser.add_argument('--version', action='version',
        version='%(prog)s ' + constants.__version__)
        
        if(not arglist):
            arglist = sys.argv[1:]
        
        args = parser.parse_args(args=arglist)
        self._argsdict = vars(args)
        return self
    
    def getencoding(self):
        return self._argsdict['e']
    
    def getinputfiles(self):
        return self._argsdict['i']
    
    def istextformat(self):
        """ Returns True if -f was passed, None otherwise """
        return self._argsdict['f']
    
    def getoutputfile(self):
        return self._argsdict['o']
    
    def istextonly(self):
        return self._argsdict['t']
    
    def iswarning(self):
        return self._argsdict['w']
    
    def iswordwrap(self):
        return self._argsdict['W']
