#! /usr/bin/python
# -*- coding:utf-8 -*
'''
Created on 2/01/2014
@author: rootmaster
'''
import os
cont = 0


def cont_line(org_file):
    global cont
    in_file = open(org_file, "r+")
    for line in in_file:
        cont += 1

    in_file.close()


def proc_file(org_file, in_char, out_char):
    con = 0
    in_file = open(org_file, "r+")
    out_file = open("out_"+org_file, "w")
    for line in in_file:
        con += 1
        print "Ejecutando procesamiento de", cont, "lineas.\n"
        print "Actualmente procesando linea No.", con
        out_file.write(line.replace(in_char, out_char))
        os.system('cls' if os.name == 'nt' else 'clear')

    in_file.close()
    out_file.close()

cont_line("trans_datos.txt")
proc_file("trans_datos.txt", "\t", ", ")
