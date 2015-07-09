#! /usr/bin/python
# -*- coding:utf-8 -*
'''
Created on 4/01/2014
@author: rootmaster
'''
import os

if __name__ == '__main__':
    os.chdir('/home/erpnext/erpnext')
    os.system('./lib/wnf.py --serve')