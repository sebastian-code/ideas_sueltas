#!/usr/bin/env python

import os
import datetime

targets = []

month = '%02d' % datetime.datetime.now().month
day = '%02d' % datetime.datetime.now().day
date = '2015%s%s' % (month, day)

front_page_template = 'http://hzdaily.hangzhou.com.cn/hzrb/page/1/2015-%s/%s/01/2015%s%s01_pdf.pdf' % (month, day, month, day)
page_template = 'http://hzdaily.hangzhou.com.cn/hzrb/page/1/2015-%s/%s' % (month, day) + '/%(page)s/%(date)s%(page)s_pdf.pdf'

a_pages = range(2, 13)
b_pages = range(1, 18)

os.system('wget %s' % front_page_template)

pdf_files = ['2015%s%s01_pdf.pdf' % (month, day)]

for page in a_pages:
    return_code = os.system('wget %s' % page_template % {'page': 'A%02d' % page, 'date': date })
    if return_code == 0:
        pdf_files.append('%sA%02d_pdf.pdf' % (date,page))

for page in b_pages:
    return_code = os.system('wget %s' % page_template % {'page': 'B%02d' % page, 'date': date })
    if return_code == 0:
        pdf_files.append('%sB%02d_pdf.pdf' % (date,page))

print(pdf_files)
os.system('pdftk %s cat output hzrb_issue_%s.pdf' % (' '.join(pdf_files), date))

for pdf_file in pdf_files:
    os.system('rm %s' % pdf_file)
