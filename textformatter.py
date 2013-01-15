# -*- coding: utf-8 -*-
import constants

__author__ = constants.__author__
__copyright__ = constants.__copyright__
__license__  = constants.__license__

class TextFormatter(object):
    """ Formats the script file with Lilith's formatting rules.
    
    Public methods:
    clear -- Reset the object to its default state
    formatline -- format a line
    
    """
    
    _isquote          = False
    _lineno           = 0
    _widewhitespace   = None
    _wideopeningchars = None
    _wideclosingchars = None
    
    def __init__(self):
        """ Constructor: Initialize required instance variables. """
        self._widewhitespace = constants.WIDE_WHITESPACE
        self._wideopeningchars = constants.WIDE_OPENING_CHARS
        self._wideclosingchars = constants.WIDE_CLOSING_CHARS
    
    def clear(self):
        """ Reset the object to its default state. """
        self._isquote = False
        self._lineno = 0
    
    def formatline(self, line):
        """ Apply formatting to the line. """
        self._lineno += 1
        line = line.rstrip(constants.NEWLINE)
        
        # Remove leading and trailing white spaces
        if(len(line.strip()) == 0):
            return line
        
        line = line.strip()
                
                
        if (self._lineno == 1 and line[0] in self._wideopeningchars):
            self._isquote = True
        
        #
        # Indentation rules
        #
        
        if (self._lineno == 1 and self._isquote):
            if (line.startswith(self._widewhitespace)):
                line = line[1:]
        
        if (self._lineno == 1 and not self._isquote):
            if (not line.startswith(self._widewhitespace)):
                line = self._widewhitespace + line
        
        # Insert double width whitespace to align lines/paragraph
        if (self._lineno > 1 and self._isquote):            
            if (not line.startswith(self._widewhitespace)):
                line = self._widewhitespace + line
            
        # If no quotation, the lines/paragraph is not aligned
        if (self._lineno > 1 and not self._isquote):
            if (line.startswith(self._widewhitespace)):
                line = line[1:]
        
        # A quote cannot end in dot '.', except in the case of ellipsis "..."
        if (self._isquote):
            for c in self._wideclosingchars:
                i = line.find(c)
                while(i != -1):
                    if(line[i - 1] == '.' and not line.endswith('...')):
                        line = line[:i - 1] + line[i:]
                    
                    i = line.find(c, i+1)
        
        
        return line + constants.NEWLINE
