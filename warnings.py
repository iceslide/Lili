# -*- coding: utf-8 -*-

import sys

import constants
import script
from utils import lenignoretag

__author__ = constants.__author__
__copyright__ = constants.__copyright__
__license__  = constants.__license__


def check(obj, filename=None, lineno=None):
    if (isinstance(obj, str)):
        return _check_line(obj, filename, lineno)
    elif (isinstance(obj, script.Block)):
        return _check_block(obj, filename)
    else:
        raise TypeError

# =================================================================

def _check_line(line, filename, lineno):
    maxlinelen = constants.MAX_LINE_LENGTH
    
    if (lenignoretag(line) > maxlinelen):
        prefix = _warn_message_prefix(filename, lineno)
        #print(':'.join(prefix + ['Line too long:']))
        _show_message(':'.join(prefix + ['Text too long ']) +
                      '(' + str(lenignoretag(line)) + '):' +
                      ''.join([line[:30], '...']))
        #print(':'.join(prefix + ['Line too long:']) +
        #      ' '.join([line[:25], '...']))

# =================================================================

def _check_block(block, filename):
    n = 0
    maxlines = constants.MAX_LINES
    
    if (len(block.gettext()) == 0):
        return
    
    for i, line in zip(block.gettextlineno(), block.gettext()):
        _check_line(line, filename, i)
        n += 1
        if (n > maxlines):
            prefix = _warn_message_prefix(filename, i)
            _show_message(
                ':'.join(prefix + ['Too many lines in message box']))
   
# =================================================================
 
def _warn_message_prefix(filename, lineno):
    prefix = []
    
    if (filename):
        prefix.append(filename)
        
    if (lineno):
        prefix.append(str(lineno))
            
    prefix.append('warning')
    return prefix

# =================================================================
    
def _show_message(message):
    print(message, file=sys.stderr)