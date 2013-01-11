#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

import sys

import liliargparser
import scriptreader
import constants

__author__ = constants.__author__
__copyright__ = constants.__copyright__
__license__  = constants.__license__

def main():
  parser = liliargparser.LiliArgParser().parse()
  
  if(len(sys.argv) == 1 or not parser.getinputfiles()):
      liliargparser.LiliArgParser().parse(['-h'])
      exit(1)
  
  #for f in parser.getinputfiles():
  #    sr = scriptreader.ScriptReader(f)
  #    sr.process()
  sr = scriptreader.ScriptReader(parser.getinputfiles())
  sr.process()

if __name__ == "__main__":
  main()
 
