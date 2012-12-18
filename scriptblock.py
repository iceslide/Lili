# -*- coding: utf-8 -*-
import liliargparser
import wrapper

class ScriptBlock(object):
    """"""
    _warning = False
    _wrapper = None
    _baselno = 0
    _lno     = 0
    _comment = [] # Commentary line indices
    _tag     = [] # Tag line indices
    _pointer = None
    _text    = []
    _maxtextlen = 68
    _block   = []
    
    def __init__(self):
        parser = liliargparser.LiliArgParser().parse()
        if (parser.iswarning()):
            self._warning = True
        if (parser.iswordwrap()):
            self._wrapper = wrapper.Wrapper()
    
    def clear(self):
        self._baselno = 0
        self._lno     = 0
        self._comment = []
        self._tag     = []
        self._pointer = None
        self._text    = []
        self._block   = []
        return self
    
    def setbaselinenumber(self, baselno):
        self._baselno = baselno
    
    def addcommentline(self, line):
        self._comment.append(self._lno)
        self._block.append(line)
        self._lno += 1
    
    def addtagline(self, line):
        self._tag.append(self._lno)
        self._block.append(line)
        self._lno += 1
    
    def addpointerline(self, line):
        self._pointer = self._lno
        self._block.append(line)
        self._lno += 1
    
    def addtextline(self, line):
        self._text.append(self._lno)
        self._block.append(line)
        self._lno += 1
        
        if (self._warning):
            if (self.lenignoretag(line) > self._maxtextlen):
                print "Warning: line", self._lno + self._baselno, "is too long"
                print self._block[-1]
        
        if (line.rstrip().endswith(u"[T_NEXT]\\") and self._wrapper != None):
            #TODO word wrap
            pass
    
    # ============================================================================
    
    def lenignoretag(self, line):
        n = 0
        level = 0
        for c in line:
            if (c == u'['): level += 1
            elif (c == u']'): level -= 1
            
            if (level == 0): n += 1
        return n
        