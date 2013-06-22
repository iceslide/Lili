# -*- coding: utf-8 -*-
import constants

__author__ = constants.__author__
__copyright__ = constants.__copyright__
__license__  = constants.__license__


def format(block):
    """ Apply formatting to a block. """
    
    wideopeningchars = constants.WIDE_OPENING_CHARS
    text = block.gettext()
    newtext = []
    isquote = False
    
    for i in range(len(text)):
        line = text[i]
        lineno = i + 1
        if (lineno == 1 and len(line) > 0 and line[0] in wideopeningchars):
            isquote = True
        newtext.append(_formatline(line, lineno, isquote))
    
    block.settext(newtext)
        

# =================================================================

def _formatline(line, lineno, isquote):
    """ Apply formatting to a line. """
    
    widewhitespace = constants.WIDE_WHITESPACE
    wideopeningchars = constants.WIDE_OPENING_CHARS
    wideclosingchars = constants.WIDE_CLOSING_CHARS
    newline = constants.NEWLINE
    #has_newline = line.endswith(newline)
    
    if(line.strip() == ''):
        # Empty line or filled with whitespaces
        return line
    
    line = line.rstrip()
        
    #
    # Indentation rules
    #
    
    # Remove leading normal white spaces
    while (line.startswith(' ')):
        line = line[1:]
    
    #
    if (lineno == 1 and isquote):
        while (line[0] not in wideopeningchars):
            line = line[1:]
    
    if (lineno == 1 and not isquote):
        if (not line.startswith(widewhitespace)):
            line = widewhitespace + line
        
    # Insert double width whitespace to align lines/paragraph
    if (lineno > 1 and isquote):            
        if (not line.startswith(widewhitespace)):
            line = widewhitespace + line
        
    # If no quotation, the lines/paragraph is not aligned
    if (lineno > 1 and not isquote):
        if (line.startswith(widewhitespace)):
            line = line[1:]
        
    # A quote cannot end in dot '.', except in the case of ellipsis "..."
    if (isquote):
        for c in wideclosingchars:
            i = line.find(c)
            while(i != -1):
                if(line[i - 1] == '.' and not line.endswith('...')):
                    line = line[:i - 1] + line[i:]
                
                i = line.find(c, i+1)
        
    #if (has_newline):
    #    line = line + constants.NEWLINE
    
    return line