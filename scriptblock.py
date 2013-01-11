# -*- coding: utf-8 -*-
from __future__ import print_function

import liliargparser
import wrapper
import textformatter
import constants

__author__ = constants.__author__
__copyright__ = constants.__copyright__
__license__  = constants.__license__

class ScriptBlock(object):
    """ This object represents a script block.
    
    A block is defined as a sequence of lines where the beginning of
    the first line start with '*' until the beginning og the next block.
    When a file starts with a comment symbol ';', all the lines until
    a '*' is found is also a  block.
    
    Public methods:
    clear -- Reset the object to its default state
    setbaselinenumber -- set the starting line of the block
    addcommentline -- add a comment line
    addtagline -- add a tag line
    addcommandline -- add a command line
    addlabelline -- add a label line
    addtextline -- add a text line
    write -- apply changes and write to output file
    
    """
    
    # Flags
    _warning       = False
    _textonly      = False
    
    
    # Objects
    _wrapper       = None
    _textformatter = None
    
    # Imported constanst
    _inputfile     = u""
    _maxlinelen    = None
    _maxlines      = None
    
    # State representation
    _baselineno    = None
    _lineno        = 0
    _block         = []
    _comment       = []  # Commentary line indices
    _tag           = []  # Tag line indices
    _command       = []  # Tag line indices
    _label         = None
    _text          = []
    
    def __init__(self, filename):
        """ Constructor: Initialize required instance variables. """
        self._inputfile = filename
        self._maxlines = constants.MAXLINES
        self._maxlinelen = constants.MAXLINELENGTH
                
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
        """ Reset the object to its default state. """
        self._baselineno = None
        self._lineno     = 0
        self._comment    = []
        self._tag        = []
        self._command    = []
        self._label      = None
        self._text       = []
        self._block      = []
        return self
        
    # =================================================================
    
    def setbaselinenumber(self, baselineno):
        """ Sets the line number starting a block """
        # Substract 1 so that baselineno + lineno points to the right line
        self._baselineno = baselineno - 1
    
    def addcommentline(self, line):
        """ Insert a comment line.
        
        A comment line begins with the character ';'.
        
        """
        self._lineno += 1
        self._comment.append(self._lineno)
        self._block.append(line)
    
    def addtagline(self, line):
        """ Insert a tag line.
        
        A tag line begins with the character '['.
        
        """
        self._lineno += 1
        self._tag.append(self._lineno)
        self._block.append(line)
    
    def addcommandline(self, line):
        """ Insert a command line.
        
        A command line begins with the character '@'.
        
        """
        self._lineno += 1
        self._command.append(self._lineno)
        self._block.append(line)
    
    def addlabelline(self, line):
        """ Insert a label line.
        
        A label line begins with the character '*'.
        
        """
        self._lineno += 1
        self._label = self._lineno
        self._block.append(line)
    
    def addtextline(self, line):
        """ Insert a text line.
        
        All lines that are not a comment, tag, command or label.
        
        """
        self._lineno += 1
        
        # Special cases (Avoid if possible)
        # Don't process line as text
        #if (line[:4] == u"===="):
        #    self._block.append(line)
        #    return
        
        self._text.append(self._lineno)
        self._block.append(line)
        
        if (self._warning):
            if (self._lenignoretag(line) > self._maxlinelen):
                print(self._inputfile, self._baselineno + self._lineno,
                      u" warning", u" Line too long:", sep=u':', end=u'')
                print(u' ', self._block[-1][:25], u"...")
            
            if (len(self._text) > self._maxlines):
                print(self._inputfile, self._baselineno + self._lineno,
                      u" warning", u" Too many lines in message box",
                      sep=u':')
    
    # =================================================================
    
    def _lenignoretag(self, line):
        """ Gets the length of a line ignoring any inline tag. """
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
    
    # =================================================================
    
    def write(self, file_, encoding):
        """ Writes the block to a file
        
        Write to file applying the wrapper or formatter if specified.
        
        """
        # Wrap text if word wrapping is enabled
        if (self._wrapper is not None and len(self._text) != 0):
            newtext = self._wrapper.wrap(self._block[-len(self._text):],
                                         self._baselineno + self._text[0])
            
            #print("newtext:", newtext)
            #print("block:", self._block)
            #print(self._block[:-len(self._text)] + newtext)
            self._block = self._block[:-len(self._text)] + newtext
            if(len(self._text) != 0):
                self._text = range(self._text[0],
                                   self._text[0] + len(newtext))
            #print("1", self._block)
        
        # Format text if text formatting is enabled
        if(self._textformatter is not None and len(self._text) != 0):
            newtext = map(self._textformatter.formatline,
                          self._block[-len(self._text):])
            #if (newtext != self._block[-len(self._text):]):
            #    print(self._baselineno + self._lineno)
            self._textformatter.clear()
            self._block = self._block[:-len(self._text)] + newtext
            #print("Newtext", newtext)
        
        f = open(file_, 'a')
        
        lines = []
        if(self._textonly):
            if(len(self._text) != 0):
                lines = map(self._writeline, self._block[-len(self._text):])
        else:
            lines = map(self._writeline, self._block)
        
        for line in lines:
            f.write(line.encode(encoding))
        
        f.close()
    
    # =================================================================
        
    def _writeline(self, line):
        """ Concatenates the strings stored in a list. """
        str_ = u''
        for word in line:
            str_ += word
        return str_
    