# -*- coding: utf-8 -*-
import liliargparser
import wrapper
import textformatter

class ScriptBlock(object):
    """"""
    _warning = False
    _wrapper = None
    _textformatter = None
    _textonly      = False
    _baselno = 0
    _lno     = 0
    _comment = [] # Commentary line indices
    _tag     = [] # Tag line indices
    _pointer = None
    _text    = []
    _maxlinelen = 68
    _maxlines   = 3 # max lines in a text block
    _block   = []
    
    def __init__(self):
        # Empty output file
        #f = open("out.txt", 'w')
        #f.close()
        
        parser = liliargparser.LiliArgParser().parse()
        if (parser.iswarning()):
            self._warning = True
        if (parser.iswordwrap()):
            self._wrapper = wrapper.Wrapper()
        if (parser.istextformat()):
            self._textformatter = textformatter.TextFormatter()
        if (parser.istextonly()):
            self._textonly = True
    
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
            if (self.lenignoretag(line) > self._maxlinelen + 1):
                print "Warning: line", self._lno + self._baselno - 1, "is too long,", self.lenignoretag(line), "characters"
                print self._block[-1]
            
            if (len(self._text) > self._maxlines):
                print "Warning: line", self._lno + self._baselno - 1, "Too many lines in the message box"
    
    # ============================================================================
    
    def lenignoretag(self, line):
        n = 0
        level = 0
        for c in line.rstrip():
            if (c == u'['): level += 1
            elif (c == u']'): level -= 1
            
            if (level == 0): n += 1
        return n
    
    # ============================================================================
    
    def write(self, file_, encoding):
        # Wrap text if word wrapping is enabled
        if (self._wrapper != None and len(self._text) != 0):
            newtext = self._wrapper.wrap(self._block[-len(self._text):])
            self._wrapper.clear()
            #print "newtext:", newtext
            #print "block:", self._block
            #print self._block[:-len(self._text)] + newtext
            self._block = self._block[:-len(self._text)] + newtext
            if(len(self._text) != 0):
                self._text = range(self._text[0], self._text[0]+len(newtext))
            #print "1", self._block
        
        # Format text if text formatting is enabled
        if(self._textformatter != None and len(self._text) != 0):
            newtext = map(self._textformatter.formatline, self._block[-len(self._text):])
            #if (newtext != self._block[-len(self._text):]):
            #    print self._baselno + self._lno - 1
            self._textformatter.clear()
            self._block = self._block[:-len(self._text)] + newtext
            #print "Newtext",newtext
        
        f = open(file_, 'a')
        
        lines = []
        if(self._textonly and len(self._text) != 0):
            lines = map(self.__writeline__, self._block[-len(self._text):])
        elif(not self._textonly):
            lines = map(self.__writeline__, self._block)
        
        for line in lines:
            f.write(line.encode(encoding))
        
        f.close()
    
    def __writeline__(self, line):
        str_ = u''
        for word in line:
            str_ += word
        return str_