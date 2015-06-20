#!/usr/bin/env python

import os

targets = []

day = '28'
date = '201505%s' % day

page_template = 'http://hzdaily.hangzhou.com.cn/dszb/page/545/2015-05/%s' %day + '/%(page)s/%(date)s%(page)s_pdf.pdf'

a_pages = range(1, 33)
b_pages = range(1, 37)

pdf_files = []

for page_a in a_pages:
    return_code = os.system('wget %s' % page_template % {'page': 'A%02d' % page_a, 'date': date })
    if return_code == 0:
        pdf_files.append('%sA%02d_pdf.pdf' % (date,page_a))

for page_a in b_pages:
    os.system('wget %s' % page_template % {'page': 'B%02d' % page_a, 'date': date })
    if return_code == 0:
        pdf_files.append('%sB%02d_pdf.pdf' % (date,page_a))

print(pdf_files)
os.system('pdftk %s cat output dszb_issue-%s.pdf' % (' '.join(pdf_files), date))
for pdf_file in pdf_files:
    os.system('rm %s' % pdf_file)
