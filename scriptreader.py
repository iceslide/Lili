#!/usr/bin/python
# -*- coding: utf-8 -*-
import fileinput
import scriptblock

class ScriptReader(object):
    """
    """
    _filename  = u''
    _encoding  = None
    _lno       = 0      # Line number
    _block     = None   # ScriptBlock
  
    def __init__(self, filename, encoding="sjis"):
        """ Constructor """
        self._filename = filename
        self._encoding = encoding
        self._lno = 0
        return None
  
    def process(self):
        self._block = scriptblock.ScriptBlock()
        self._block.setbaselinenumber(self._lno)
        # Check if scriptreader-fileinput works correctly in py3
        with open(self._filename, 'r') as f:
            for line in f:
                line = line.decode(self._encoding)
                self._lno += 1
                
                #if (self._lno < 300):
                #    continue
                #elif (self._lno > 310):
                #    return
                #print self._lno, line
                
                if (line[0] == ';'):
                    self._block.addcommentline(line)
                elif (line[0] == '['):
                    self._block.addtagline(line)
                elif (line[0] == '*'):
                    # TODO Process old block before clearing it
                    self._block.clear().setbaselinenumber(self._lno)
                    self._block.addpointerline(line)
                else:
                    # Game text
                    self._block.addtextline(line)
        
        print self._lno, "lines processed"