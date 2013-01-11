#!/usr/bin/python
# -*- coding: utf-8 -*-
import fileinput
import scriptblock

class ScriptReader(object):
    """
    """
    _inputfile = u''
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
        # This iterates over the lines of all files listed in sys.argv[1:]
        for line in fileinput.input(openhook=fileinput.hook_encoded(self._encoding)):
            #self._lno += 1
            self._lno = fileinput.lineno()
            if (self._lno < 300):
                continue
            elif (self._lno > 310):
                return
            
            print self._lno, line
            
            if (line[0] == ';'):
                self._block.addcommentline(line)
            elif (line[0] == '['):
                self._block.addtagline(line)
            elif (line[0] == '*'):
                # Process old block and create new one
                # TODO something
                self._block.clear().setbaselinenumber(self._lno)
                self._block.addpointerline(line)
            else:
                # Game text
                self._block.addtextline(line)
    
        print self._lno, "lines processed"