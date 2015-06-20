#!/usr/bin/env python

import os
import sys

icon_name = "icon"

if len(sys.argv) == 2:
    icon_name = sys.argv[1]

size_list = ['16x16', '32x32', '128x128', '256x256', '512x512']

for index, size in enumerate(size_list):
    os.system('convert -resize %s %s_512x512@2x.png %s_%s.png' % (size, icon_name, icon_name, size))
    if index > 0:
        os.system('convert -resize %s %s_512x512@2x.png %s_%s@2x.png' % (size, icon_name, icon_name, size_list[index - 1]))
