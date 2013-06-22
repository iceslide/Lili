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
            help='specify the input file encoding. Default: shift_jis. \
                  For more encodings visit \
                  http://docs.python.org/3/library/codecs.html#standard-encodings')
        #parser.add_argument('-i', type=str, action="store", help='input file')
        parser.add_argument('i', type=str, action="store", nargs='+',
            help='input files')
        parser.add_argument('-f', action='store_true',
            help='format the file following Lilith\'s style guidelines')
        parser.add_argument('-o', type=str,
            help='output file. If not specified, the changes \
                  will be written to standard output')
        parser.add_argument('-s', action='store_true',
            help='Linear substitution of the text in file1 \
                  with the text from file2')
        parser.add_argument('-t', action='store_true',
            help='output only the game text')
        parser.add_argument('-v', action='store_true', help='verbose')
        parser.add_argument('-w', action='store_true',
            help='enables warnings related to the text presentation \
                  inside the message box')
        parser.add_argument('-W', action='store_true',
            help='basic word wrapping')
        parser.add_argument('--version', action='version',
        version='%(prog)s ' + constants.__version__)
        
        if(not arglist):
            arglist = sys.argv[1:]
        
        args = parser.parse_args(args=arglist)
        self._argsdict = vars(args)
        return self
    
    def getencoding(self):
        return self._argsdict['e']
    
    #def getinputfile(self):
    #    return self._argsdict['i']
    
    def getinputfiles(self):
        return self._argsdict['i']
    
    def format_enabled(self):
        """ Returns True if -f was passed, None otherwise """
        return self._argsdict['f']
    
    def getoutputfile(self):
        return self._argsdict['o']
    
    def substitute_enabled(self):
        return self._argsdict['s']
    
    def text_only(self):
        return self._argsdict['t']
    
    def verbose_enabled(self):
        return self._argsdict['v']
    
    def warning_enabled(self):
        return self._argsdict['w']
    
    def wordwrap_enabled(self):
        return self._argsdict['W']
