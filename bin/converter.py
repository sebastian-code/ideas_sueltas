#!/usr/bin/python

import os
import glob

to_converted = glob.glob('*.JPG')
to_converted.sort()

print("Please enter the prefix: %s")
prefix = raw_input()

for i, name in enumerate(to_converted):
    print('convert -resize 550x413 %s %s/%s-%d.jpg' % (name, prefix, prefix, i))
    os.system('convert -resize 550x413 %s %s/%s-%d.jpg' % (name, prefix, prefix, i))
#    os.system('convert -resize 1024x768 %s/%s-%d.jpg' % (name, prefix, prefix, i))
