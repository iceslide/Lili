#!/usr/bin/python
# -*- coding: utf-8 -*-
#import fileinput
import scriptblock
import liliargparser

class ScriptReader(object):
    """
    """
    _inputfile      = u''
    _outputfile     = u"out.txt"
    _encoding       = u"sjis"
    _lineno         = 0      # Line number
    _block          = None   # ScriptBlock
  
    def __init__(self, filename):
        """ Constructor """
        self._inputfile = filename
        self._lineno    = 0
        
        parser = liliargparser.LiliArgParser().parse()
        if (parser.getencoding()):
            self._encoding = parser.getencoding()
        if (parser.getoutputfile()):
            self._outputfile = parser.getoutputfile()[0]
                
        return None
  
    def process(self):
        self._block = scriptblock.ScriptBlock()
        self._block.setbaselinenumber(self._lineno)
        
        # Empty the output file
        fout = open(self._outputfile, 'w')
        fout.close()
        
        # Check if scriptreader-fileinput works correctly in py3
        with open(self._inputfile, 'r') as f:
            for line in f:
                line = line.decode(self._encoding)
                self._lineno += 1
                
                #if (self._lineno < 300):
                #    continue
                #elif (self._lineno > 310):
                #    return
                #print self._lineno, line
                
                if (line[0] == ';'):
                    self._block.addcommentline(line)
                elif (line[0] == '[' or line[0] == '@'):
                    self._block.addtagline(line)
                elif (line[0] == '*'):
                    # Process old block before clearing it
                    self._block.write(self._outputfile, self._encoding)
                    self._block.clear().setbaselinenumber(self._lineno)
                    # New block
                    self._block.addpointerline(line)
                else:
                    # Game text
                    self._block.addtextline(line)
        
        self._block.write(self._outputfile, self._encoding)
        
        print self._lineno, "lines processed"