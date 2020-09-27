#!/usr/bin/env python

import os
import glob

for path in glob.glob("*"):
    locale_path = os.path.join(path, "LC_MESSAGES/django.po")
    if os.path.exists(locale_path):
        os.rename(locale_path, "%s.po" % path)
