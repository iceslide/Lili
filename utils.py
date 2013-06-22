# -*- coding: utf-8 -*-
import constants

def lenignoretag(line):
    """ Gets the length of a line ignoring any inline tag. """
    n = 0
    level = 0
    for c in line.rstrip(constants.NEWLINE):
        if(level < 0):
            # Check for case ']\'
            if (c == '\\'):
                continue
            else:
                level = abs(level) - 1
        elif (c == '['):
            level += 1
            continue
        elif (c == ']'):
            level = -level
            continue
       
        if (level == 0):
            n += 1
    
    return n