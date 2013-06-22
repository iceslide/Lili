# -*- coding: utf-8 -*-
import sys

import constants

__author__ = constants.__author__
__copyright__ = constants.__copyright__
__license__  = constants.__license__


# =================================================================
# Class Reader
# =================================================================

class Reader(object):
    """ Reads blocks from a script file.
    
    Public methods:
    read -- Returns a generator to read the stream
    readblock -- Returns a block from the stream
    
    """
    
  
    def __init__(self, filename, encoding=constants.DEFAULT_ENCODING):
        """ Constructor: Initialize required instance variables. """
        
        # Although not necessary now, it is left to remind that problems
        # arise with python's memory reutilization. Creating a new instance
        # inside a loop, self._data kept the text of all the previous files.
        self._reset()
        
        self._filename = filename
        
        #newline=constants.NEWLINE
        with open(self._filename, 'rt',
                  encoding=encoding, newline=None) as f:
            self._data = [(lineno, line.rstrip()) for lineno, line in enumerate(f, 1)]
            
        #with open(self._filename, 'rb') as f:
            #self._data = [(lineno, line.decode(encoding))
            #              for lineno, line in enumerate(f, 1)]
            #for lineno, line in enumerate(f, 1):
            #    self._data.append((lineno, line.decode(encoding)))            
   
    # =================================================================
    
    def _reset(self):
        """ Resets the class variables to its initial state """
        
        self._filename = None
        self._data = []       # List of 2-tuple(lineno, line)
        self._i = 0           # Block start index
    
    # =================================================================  
    
    def read(self):
        """  Returns a generator to read the whole stream """
        
        self._i = 0 # We want to read the whole stream
        while (self._i < len(self._data) - 1):
            yield self.readblock()
            
    
    # =================================================================
    
    def readblock(self):
        """  Returns a block from the stream """
        
        if (self._i > len(self._data) - 1):
            return None
        
        is_end = False
        is_text = False
        n = 0
        block = Block(self._filename, self._data[self._i][0])

        while (not is_end):
                
            line = self._data[self._i + n][1]
            n += 1 
            
            # Consider comments, commands, and tags intertwined with text
            # as text for easier manipulation
            if (not is_text and line.startswith(';')):
                block.addcommentline(line)
            elif (not is_text and line.startswith('[')):
                block.addtagline(line)
            elif (not is_text and line.startswith('@')):
                block.addcommandline(line)
            elif (line.startswith('*')):
                block.addlabelline(line)
            else:
                # Game text
                is_text = True
                block.addtextline(line)
            
            # End of block?
            if ((self._i + n) > (len(self._data) - 1) or 
                self._data[self._i + n][1].startswith('*')):
                is_end = True
                self._i += n
    
        return block





# =================================================================
# Class Writer
# =================================================================
 
class Writer(object):
    """ Reads blocks from a script file.
    
    Public methods:
    write -- Writes a block to a file or to stdout if none is specified 
    
    """
    _file = None # If not declared here it won't work
  
    def __init__(self, filename=None, encoding=constants.DEFAULT_ENCODING):
        """ Constructor: Initialize required instance variables. """
        
        self._reset()
        self._filename = filename
        self._encoding = encoding
        
        if (filename):
            # create or empty file if it exists
            f = open(self._filename, 'wb')
            f.close()
            
            self._file = open(self._filename, 'ab')
   
    # =================================================================
    
    def _reset(self):
        """ Resets the class variables to its initial state """
        
        self._filename = None
        self._encoding = None
        
        if (self._file):
            self._file.close()
        
        self._file = None
    
    # =================================================================  
    
    def write(self, block, textonly=False):
        """ Writes a block to a file or to stdout if none is specified
        
        If the textonly flag is active, only the game text will be written
        
        """
        
        if(not isinstance(block, Block)):
            raise TypeError
        
        if(textonly):
            self._write_text(block)
        else:
            self._write_block(block)
        
    # =================================================================  
    
    def _write_text(self, block):
        """ Writes a block to a file or to stdout if none is specified """
        
        newline = constants.NEWLINE
        text = newline.join([line for line in block.gettext()]) + newline
        if(self._file):
            byte_str = bytes(text, self._encoding)
            self._file.write(byte_str)
        else:
            sys.stdout.write(text)   
        
        
   # =================================================================  
    
    def _write_block(self, block):
        """ Writes a block to a file or to stdout if none is specified """
        
        
        if(self._file):
            byte_str = bytes(block.tostr(), self._encoding)
            self._file.write(byte_str)
        else:
            sys.stdout.write(block.tostr())
        
        
        
        
# =================================================================
# Class Block
# =================================================================

class Block(object):
    """ This object represents a script block.
    
    A block is defined as a sequence of lines where the beginning of
    the first line start with '*' until the beginning og the next block.
    When a file starts with a comment symbol ';', all the lines until
    a '*' is found is also a  block.
    
    Public methods:
    addcommentline -- add a comment line
    addtagline -- add a tag line
    addcommandline -- add a command line
    addlabelline -- add a label line
    addtextline -- add a text line
    getlabel -- Returns the label
    gettext -- Returns the text
    gettextlineno -- Returns the text line numbers
    settext -- Set the block's text
    tostr -- Returns a string representation of the block data
    
    """
    
    LABEL = 'label'
    TEXT  = 'text'
    
    def __init__(self, filename, baselineno=0):
        """ Constructor: Initialize required instance variables """
        
        self._reset()
        
        self._filename = filename
        self._baselineno = baselineno
    
    # =================================================================
    
    def _reset(self):
        """ Resets the class variables to its initial state """
        
        self._filename = None   
        self._baselineno = 0
        self._lineno = 0
        self._data = []
        self._index = {}     # Dictionary with indices for each component
        
    # =================================================================
    
    def addcommentline(self, line):
        """ Insert a comment line.
        
        A comment line begins with the character ';'.
        
        """
        self._data.append(line)
        self._lineno += 1
        
    # =================================================================
    
    def addtagline(self, line):
        """ Insert a tag line.
        
        A tag line begins with the character '['.
        
        """
        self._data.append(line)
        self._lineno += 1
                
        
    # =================================================================
    
    def addcommandline(self, line):
        """ Insert a command line.
        
        A command line begins with the character '@'.
        
        """
        self._data.append(line)
        self._lineno += 1
        
        
    # ================================================================= 
    
    def addlabelline(self, line):
        """ Insert a label line.
        
        A label line begins with the character '*'.
        
        """
        self._data.append(line)
        
        try:
            self._index[self.LABEL] += self._lineno
        except KeyError:
            self._index[self.LABEL] = self._lineno
        
        self._lineno += 1
        
        
    # =================================================================
    
    def addtextline(self, line):
        """ Insert a text line.
        
        All lines that are not a comment, tag, command or label.
        
        """
        self._data.append(line)
        
        #try:
        #    self._index[self.TEXT] += (self._lineno,)
        #except KeyError:
        #    self._index[self.TEXT] = (self._lineno,)
        
        # Which is faster/better?
        if (self.TEXT in self._index):
            self._index[self.TEXT] += (self._lineno,)
        else:
            self._index[self.TEXT] = (self._lineno,)
        
        self._lineno += 1

    # =================================================================
    
    def getlabel(self):
        """ Returns the label """
        
        if (self.LABEL in self._index):
            i = self._index.get(self.LABEL)
            return self._data[i]
        else:
            return ''
    
    # =================================================================
    
    def gettext(self):
        """ Returns the text """
        
        if (self.TEXT in self._index):
            return [self._data[i] for i in self._index.get(self.TEXT)]
        else:
            return []
    
    # =================================================================
    
    def gettextlineno(self):
        """ Returns the text line numbers """
        
        if (self.TEXT in self._index):
            return [self._baselineno + i for i in self._index.get(self.TEXT)]
        else:
            return tuple()
    
    # =================================================================
    
    def hastext(self):
        """ Returns True if the block contains text, False otherwise """
        if self.TEXT in self._index:
            return True
        else:
            return False
    
    # =================================================================
    
    def settext(self, text):
        """ Set the block's text """
        
        if (not self.hastext()):
            return
        
        i = self._index.get(self.TEXT)[0]
        j = self._index.get(self.TEXT)[-1]
        
        self._data = self._data[:i] + text + self._data[j+1:]
        self._index[self.TEXT] = tuple(range(i, i+len(text)))
    
    # =================================================================
    
    def tostr(self):
        """ Returns a string representation of the block data """
        
        newline = constants.NEWLINE
        return newline.join([line for line in self._data]) + newline
        #return '\r\n'.join([line.rstrip() for line in self._data]) + '\r\n'
        #return ''.join(self._data)
