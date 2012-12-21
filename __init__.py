#!/usr/bin/python
# -*- coding: utf-8 -*-
#import sys
import liliargparser
import scriptreader

def main():
  parser = liliargparser.LiliArgParser().parse()
  
  for f in parser.getinputfiles():
      sr = scriptreader.ScriptReader(f)
      sr.process()

if __name__ == "__main__":
  main()
 
