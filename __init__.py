#!/usr/bin/python
# -*- coding: utf-8 -*-
#import sys
import liliargparser
import scriptreader

def main():
  parser = liliargparser.LiliArgParser().parse()
  encoding = parser.getencoding()
  
  for f in parser.getinputfiles():
      sr = None
      
      if (encoding != None): sr = scriptreader.ScriptReader(f, encoding)
      else:                  sr = scriptreader.ScriptReader(f)
      
      sr.process()

if __name__ == "__main__":
  main()
 
