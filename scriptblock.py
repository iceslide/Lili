# -*- coding: utf-8 -*-
import liliargparser
import wrapper
import textformatter

class ScriptBlock(object):
    """"""
    _warning       = False
    _wrapper       = None
    _textformatter = None
    _textonly      = False
    _baselineno    = None
    _lineno        = 0
    _comment       = [] # Commentary line indices
    _tag           = [] # Tag line indices
    _pointer       = None
    _text          = []
    _maxlinelen    = 58 # Value for Taimanin 2 Asagi Premium Box. Change accordingly for your game
    _maxlines      = 3 # max lines in a text block
    _block         = []
    
    def __init__(self):        
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
        self._baselineno = None
        self._lineno     = 0
        self._comment    = []
        self._tag        = []
        self._pointer    = None
        self._text       = []
        self._block      = []
        return self
        
    # ============================================================================
    
    def setbaselinenumber(self, baselno):
        self._baselineno = baselno
    
    def addcommentline(self, line):
        self._comment.append(self._lineno)
        self._block.append(line)
        # A comment block begins with a comment. Typically first block in file
        if (self._baselineno == None): self._baselineno = 0
        else:                          self._lineno    += 1
    
    def addtagline(self, line):
        self._tag.append(self._lineno)
        self._block.append(line)
        self._lineno += 1
    
    def addpointerline(self, line):
        self._pointer = self._lineno
        self._block.append(line)
        # A block begins with a pointer
        if (self._baselineno == None): self._baselineno = 0
        else:                          self._lineno    += 1
    
    def addtextline(self, line):
        
        if (line[:4] == u"===="):
            self._block.append(line)
            self._lineno += 1
            return                  # Don't process line as text
        
        self._text.append(self._lineno)
        self._block.append(line)
        self._lineno += 1
        
        if (self._warning):
            if (self.lenignoretag(line) > self._maxlinelen):
                print "[Warning][line", self._lineno + self._baselineno, "] Line is too long,", self.lenignoretag(line), "characters: ",
                print self._block[-1][:50], "..."
            
            if (len(self._text) > self._maxlines):
                print "Warning: line", self._lineno + self._baselineno, "Too many lines in the message box"
    
    # ============================================================================
    
    def lenignoretag(self, line):
        n = 0
        level = 0
        for c in line.rstrip():
            if (c == u'['):
                level += 1
                continue
            elif (c == u']'):
                level -= 1
                continue
            
            if (level == 0):
                n += 1
        
        return n
    
    # ============================================================================
    
    def write(self, file_, encoding):
        # Wrap text if word wrapping is enabled
        if (self._wrapper != None and len(self._text) != 0):
            newtext = self._wrapper.wrap(self._block[-len(self._text):], self._baselineno + self._text[0])
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
            #    print self._baselineno + self._lineno
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
    
    # ============================================================================
        
    def __writeline__(self, line):
        str_ = u''
        for word in line:
            str_ += word
        return str_