# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

__license__   = u"GPL v3"
__copyright__ = "2012, iceslide <iceslide@gmail.com>"
__appname__   = u"Lili"
_numeric_version = (0, 2)
__version__   = u'.'.join(map(unicode, _numeric_version))
__author__    = u"iceslide <iceslide@gmail.com>"


DEFAULTENCODING = u"sjis"
DEFAULTOUTPUTFILE = u"out.txt"

MAXLINES = 3        # Maximum lines in a message box
MAXLINELENGTH = 58  # Value for Taimanin 2 Asagi Premium Box.
                    # Change accordingly for your game.

NEWLINE = u"\r\n"
WIDEWHITESPACE = u'\u3000'
WIDEOPENINGCHARS = [u'「', u'（', u'『']
WIDECLOSINGCHARS = [u'」', u'）', u'』']

# Shamelessly ripped from Calibre project

""" Runtime constants"""
#import sys, locale, codecs

#_plat = sys.platform.lower()
#iswindows = 'win32' in _plat or 'win64' in _plat
#isxp = iswindows and sys.getwindowsversion().major < 6
#islinux   = not(iswindows or isosx or isbsd)

#try:
  #preferred_encoding = locale.getpreferredencoding()
  #codecs.lookup(preferred_encoding)
  #except:
    #preferred_encoding = 'utf-8'
