#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

import sys

import liliargparser
import script
import constants
import warnings
import wrapper
import formatter


__author__ = constants.__author__
__copyright__ = constants.__copyright__
__license__  = constants.__license__


def process_files():
  """ Process input files """
  
  inputfiles = None
  outputfile = None
  encoding = constants.DEFAULT_ENCODING
  
  parser = liliargparser.LiliArgParser().parse()
  
  if (parser.getinputfiles()):
      inputfiles = parser.getinputfiles()
  
  if (parser.getencoding()):
      encoding = parser.getencoding()
  
  if (parser.getoutputfile()):
      outputfile = parser.getoutputfile()
  
  # Process input files
  for f in inputfiles:
      sr = script.Reader(f, encoding)
      sw = script.Writer(outputfile)
      messagecount = 0
      
      for block in sr.read():
          if (parser.warning_enabled()):
              warnings.check(block, f)
          
          if (parser.wordwrap_enabled()):
              wrapper.wrap(block)
          
          if (parser.format_enabled()):
              formatter.format(block)
          
          if (parser.verbose_enabled()):
              if len(block.gettext()) > 0 : messagecount += 1
          
          if (not parser.warning_enabled()):
              if(parser.text_only()):
                  sw.write(block, textonly=True)
              else:
                  sw.write(block)
      
      if (parser.verbose_enabled()):
          print(f, ': ', messagecount, " text messages", sep='', file=sys.stderr)
  
# ================================================================= 

def substitute_text():
    """ Replaces the text from file1 with that of file2
    
    File 1 and file2 are arguments from the command line
    
    """
    inputfiles = None
    outputfile = None
    encoding = constants.DEFAULT_ENCODING
    
    parser = liliargparser.LiliArgParser().parse()
    
    if (parser.getinputfiles()):
        inputfiles = parser.getinputfiles()
    
    if (parser.getencoding()):
        encoding = parser.getencoding()
    
    if (parser.getoutputfile()):
        outputfile = parser.getoutputfile()
    
    if (len(inputfiles) < 2):
        exit(1)
    
    def skip_until_text(sr, write=False):
        """ Keep reading until a block with text is found """
        end = False
        while (not end):
            block = sr.readblock()
            if (not block):
                end = True
                continue
            elif (not block.hastext()):
                if (write):
                    sw.write(block)
                    continue
            else:
                return block
        
        return None
    
    # Process input files
    for target, source in [tuple(inputfiles[:2])]:
        sr_t = script.Reader(target, encoding)
        sr_s = script.Reader(source, encoding)
        sw = script.Writer(outputfile)
        
        end = False
        while (not end):
            # Skip until text found
            block_t = skip_until_text(sr_t, write=True)
            
            # Skip until text found
            block_s = skip_until_text(sr_s, write=False)
            
            # If reached end of file
            if(not block_t or not block_s):
                end = True
            else:
                # Swap text
                if (parser.verbose_enabled()):
                    print(block_t.getlabel().rstrip(),
                          '\t', block_s.getlabel().rstrip())
                
                block_t.settext(block_s.gettext())
                sw.write(block_t)
        
        # Write any remaining blocks
        block_t = sr_t.readblock()
        while(block_t):
            sw.write(block_t)
            block_t = sr_t.readblock()

# ================================================================= 

def main():
    parser = liliargparser.LiliArgParser().parse()
    
    if (parser.substitute_enabled()):
        substitute_text()
    else:
        process_files()
    
    exit(0)

# ================================================================= 

if __name__ == "__main__":
    main()
    
    
 
