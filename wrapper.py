# -*- coding: utf-8 -*-

import constants
from utils import lenignoretag

__author__ = constants.__author__
__copyright__ = constants.__copyright__
__license__  = constants.__license__


def wrap(block):
    """ Wraps a block of text
    
    Arguments:
    block -- Script block to be word wrapped
        
    """
    dowrap = False
    maxlinelen = constants.MAX_LINE_LENGTH
    newline = constants.NEWLINE
    text = block.gettext()
    
        
    # Only wrap if one or more lines exceed the max length
    if (any([lenignoretag(line) > maxlinelen for line in text])):
        dowrap = True
    
    if (not dowrap):
        return text
        
        
    # Wrap segment #
    
    tokens = [word for line in text for word in _tokenize(line)]

    line = ''
    newtext = []
    n = 0
    for t in tokens:
        if (n + lenignoretag(t) <= maxlinelen):
            n += lenignoretag(t)
            line += t
        else:
            # Line is full
            newtext.append(line.rstrip())
            n = 0
            if (t != ' '):
                line = t + ' '
                n += lenignoretag(t)
            else:
                line = ''
            
    newtext.append(line)
    newtext = [s + newline for s in newtext]
        
    #print("N:", len(newtext))
    #print("Newtext:", newtext)
    block.settext(newtext)
    
# =================================================================
    
def _tokenize(line):
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