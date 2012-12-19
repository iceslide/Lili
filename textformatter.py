# -*- coding: utf-8 -*-

class TextFormatter(object):
    """ Text formatter class to preserve the original script formatting style """
    
    _openquote        = u'「'
    _closequote       = u'」'
    _doublewidthspace = u'\u3000'
    _isquote          = False
    _lineno           = 0
    
    def __init__(self):
        pass
    
    def clear(self):
        """ Resets the object to its default state """
        self._isquote = False
        self._lineno = 0
    
    def formatline(self, line):
        """ Enforces the original script formatting style """
        self._lineno += 1
        
        if (self._lineno == 1 and line[0] == self._openquote):
            self._isquote = True
        
        # Insert double space to align lines/paragraph
        if (self._lineno > 1 and self._isquote):
            if (line[0] == u' '): line[0] = self._doublewidthspace
            elif (line[0] != self._doublewidthspace): line = self._doublewidthspace + line
        
        # If no quotation, the lines/paragraph is not aligned
        if (self._lineno > 1 and not self._isquote):
            if (line[0] == u' ' or line[0] == self._doublewidthspace ):
                line = line[1:]
        
        return line
