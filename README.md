Lili
====

Lili is a Kirikiri2/KAG3 scenario files processing tool. It provides a series
of helper utilities to aid in the translation of games based on this engine.

Lili provides the following functionality:

 - Warnings related to the message box text presentation.
 - Basic word wrapping.
 - Automatic text formatting.
 - Extracts dialog text.
 - Linear substitution of game text in one file with that from another.
   Ideal to port an existing translation to a newer game release.

License and disclaimer
----------------------
Copyright (C) 2012, 2013 iceslide <iceslide@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Lili is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE. See the GNU General Public License for more details.

Requirements
------------

This tool requires Python 3. It is developed and tested in Python 3.2


Usage examples
--------------

> ./lili.py -w file1.ks
This will print a warning when the text doesn't fit nicely inside the message box.

> ./lili.py -W -f -o out.ks file1.ks
Apply Word wrapping and text formatting. The resulting text will be written to
out.ks. If -o is not specified it'll be written to the standard output.

> ./lili.py -t -o out.ks file1.ks
Outputs only the game text.

> ./lili.py -s -o out.ks file1.ks file2.ks
Replaces the text in file1 with that found in file2. If -v is also passed as
argument, the labels of the resulting matches will be printed to standard
output.
