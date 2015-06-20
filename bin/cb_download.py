#!/usr/bin/env python

import os
import datetime

targets = []

day = str(datetime.datetime.now().day)
date = '201505%s' % day

page_template = 'http://hzdaily.hangzhou.com.cn/cb/page/1681/2015-05/%s' %day + '/%(page)s/%(date)s%(page)s_pdf.pdf'

pages = range(1, 25)

pdf_files = ['%s01_pdf.pdf' % date]

for page in pages:
    return_code = os.system('wget %s' % page_template % {'page': '%02d' % page, 'date': date })
    if return_code == 0:
        pdf_files.append('%s%02d_pdf.pdf' % (date,page))

print(pdf_files)
os.system('pdftk %s cat output cb_issue_%s.pdf' % (' '.join(pdf_files), date))

for pdf_file in pdf_files:
    os.system('rm %s' % pdf_file)
