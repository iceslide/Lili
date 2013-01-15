# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

__license__   = "GPL v3"
__copyright__ = "2012, iceslide <iceslide@gmail.com>"
__appname__   = "Lili"
_numeric_version = (0, 3)
__version__   = '.'.join(map(str, _numeric_version))
__author__    = "iceslide <iceslide@gmail.com>"


DEFAULT_ENCODING = "shift_jis"
DEFAULT_OUTPUT_FILE = "out.txt"

MAX_LINES = 3        # Maximum lines in a message box
MAX_LINE_LENGTH = 58  # Value for Taimanin 2 Asagi Premium Box.
                    # Change accordingly for your game.

NEWLINE = "\r\n"
WIDE_WHITESPACE = '\u3000'
WIDE_OPENING_CHARS = ['「', '（', '『']
WIDE_CLOSING_CHARS = ['」', '）', '』']