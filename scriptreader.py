#!/usr/bin/python
# -*- coding: utf-8 -*-
#import fileinput
from __future__ import print_function

import scriptblock
import liliargparser
import constants

__author__ = constants.__author__
__copyright__ = constants.__copyright__
__license__  = constants.__license__

class ScriptReader(object):
    """ Reads the contents of a file and process each block.
    
    Public methods:
    process -- process the input file
    
    """
    
    _inputfile      = u""
    _outputfile     = u"out.txt"
    _encoding       = u"sjis"
    _lineno         = 0      # Line number
    _block          = None   # ScriptBlock
  
    def __init__(self, filename):
        """ Constructor: Initialize required instance variables. """
        self._inputfile = filename
        self._lineno = 0
        
        parser = liliargparser.LiliArgParser().parse()
        if (parser.getencoding()):
            self._encoding = parser.getencoding()
        else:
            self._encoding = constants.DEFAULTENCODING
        
        if (parser.getoutputfile()):
            self._outputfile = parser.getoutputfile()
        else:
            self._outputfile = constants.DEFAULTOUTPUTFILE
            #self._outputfile = self._inputfile + "~lili"
                
        return None
  
    def process(self):
        """ Process the file specified in the constructor
            and writes the result to the output file
        """
        self._block = scriptblock.ScriptBlock(self._inputfile)
        self._block.setbaselinenumber(self._lineno)
        
        # Empty the output file
        fout = open(self._outputfile, 'w')
        fout.close()
        
        # Check if scriptreader-fileinput works correctly in py3
        with open(self._inputfile, 'r') as f:
            for line in f:
                line = line.decode(self._encoding)
                self._lineno += 1
                
                if (line.startswith(u';')):
                    self._block.addcommentline(line)
                elif (line.startswith(u'[')):
                    self._block.addtagline(line)
                elif (line.startswith(u'@')):
                    self._block.addcommandline(line)
                elif (line.startswith(u'*')):
                    # Process old block before clearing it
                    self._block.write(self._outputfile, self._encoding)
                    self._block.clear().setbaselinenumber(self._lineno)
                    # New block
                    self._block.addlabelline(line)
                else:
                    # Game text
                    self._block.addtextline(line)
        
        self._block.write(self._outputfile, self._encoding)
        
        #print(self._inputfile,
        #      str(self._lineno) + u" lines processed", sep=u':')