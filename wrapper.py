# -*- coding: utf-8 -*-
from __future__ import print_function

import constants

__author__ = constants.__author__
__copyright__ = constants.__copyright__
__license__  = constants.__license__

class Wrapper(object):
    """ Wraps the text to avoid overflowing the message box.
    
    Public methods:
    wrap -- Perform the wrapping
    
    """
    
    _newline    = None
    _maxlinelen = None
    _maxlines   = None
    
    _textlines  = []
    _baselineno = None
    
    def __init__(self):
        """ Constructor: Initialize required instance variables. """
        self._newline = constants.NEWLINE
        self._maxlines = constants.MAX_LINES
        self._maxlinelen = constants.MAX_LINE_LENGTH
    
    
    def wrap(self, textlines, baselineno):
        """ Wraps a block of text
        
        Arguments:
        textlines -- the list of strings to wrap
        baselineno -- the line number of the first line
        
        """
        self._textlines = textlines
        self._baselineno = baselineno
        dowrap = False
        
        # Only wrap if one or more lines exceed the max length
        for line in self._textlines:
            #print(self._lenignoretag(line))
            if (self._lenignoretag(line) > self._maxlinelen):
                dowrap = True;
                break
        
        if (not dowrap):
            return self._textlines
            #print("map", map(self._tokenize, self._textlines)f._textlines)
        
        # Wrap segment
        tokens = list(map(self._tokenize, self._textlines))
        
        # Flatten tokens list
        flattokens = []
        for i in range(len(tokens)):
            flattokens += tokens[i]
        #print("Flattokens", flattokens)
        
        # Wrap loop
        tmp = []
        newtokens = []
        n = 0
        for t in flattokens:
            if (n + self._lenignoretag(t) <= self._maxlinelen):
                n += self._lenignoretag(t)
                tmp.append(t)
            else:
                # Line is full
                newtokens.append(tmp)
                n = 0
                if (t != ' '):
                    tmp = [t]
                    n += self._lenignoretag(t)
                else:
                    tmp = []
                
        newtokens.append(tmp)
        
        #print("N:", len(newtokens))
        #print("Newtokens:", newtokens)
        return self._tokenstostringlist(newtokens)
    
    # =================================================================
    
    def _lenignoretag(self, line):
        """ Gets the length of a line ignoring any inline tag. """
        n = 0
        level = 0
        for c in line:
            if (c == '['):
                level += 1
                continue
            elif (c == ']'):
                level -= 1
                continue
            
            if (level == 0):
                n += 1
                
        return n
    
    # =================================================================
    
    def _tokenstostringlist(self, tokens):
        """ Returns a list containing a string.
        
        Receives a list of lists of tokens and returns a list
        with the final string with newlines characters inserted.
        
        """
        lines = []
        #print("Token:", tokens)
        for tokenlist in tokens:
            line = ""
            for word in tokenlist:
                line += word
            line += self._newline
            lines.append(line)
        #print("lines:", lines)
        return lines
    
    # =================================================================
    
    def _tokenize(self, line):
        """ Returns a list of tokens.
        
        Breaks the line into tokens: wide spaces, spaces, words and tags.
        Removes trailing whitespace characters, and
        returns a list of tokens represented by their string values.
        
        """
        T = []
        level = 0
        token_ini = 0
        s = ""
        
        for i in range(len(line)):
            if(line[i] == '\u3000' and level == 0):
                # Detect word
                s = line[token_ini:i]
                if(len(s) > 0):
                    T.append(s)
                T.append('\u3000')
                token_ini = i + 1
            elif(line[i] == ' ' and level == 0):
                # Detect word
                s = line[token_ini:i]
                if(len(s) > 0):
                    T.append(s) #single word
                T.append(' ')
                token_ini = i + 1
            elif(line[i] == ',' and level == 0):
                # Detect word
                s = line[token_ini:i+1]
                T.append(s) #single word
                token_ini = i + 1
            elif(line[i] == '['):
                # Detect start tag
                level += 1
                T.append(line[token_ini:i])
                token_ini = i
            elif(line[i] == ']'):
                # Detect end tag
                level -= 1
                T.append(line[token_ini:i+1])
                token_ini = i + 1
            else:
                pass
                                    
        s = line[token_ini:len(line)].rstrip()
        if(len(s) > 0):
            T.append(s)
                                        
        #print("Tokens:", len(T))
        #print(T)
        return T