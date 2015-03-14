#! /usr/bin/python
# -*- coding:utf-8 -*-
'''
Created on 06/12/2013
@note: Demonio infito.
@summary: Demonio para comunicaciones puerto serial AsahiKASEI MDS-101.
@author: Sebastian Reyes Espinosa.
@organization: Técnica Humana S.A.S. 
@version: v0.1
'''

import sys
import serial
import threading
import time

# Variable para indicar al thread que termine
fin = 0

# Este hilo se ejecuta infinitamente. Lee datos del puerto serie y sacandolos por la consola
bd = open("salida.txt", "a")

def reader():
    while not(fin):
        try:
            data = s.read()
            sys.stdout.write(data)
            sys.stdout.flush()
            bd.write(data)
            bd.flush()
            
        except:
            print "Excepcion: Abortando..."
            bd.close()
            break;       
 
# Este es el bucle principal, la cadena del tipo "K\r\n" por la consola se envia por el puerto serie.

def writer():
    while 1:
        try:
            while 1:
                s.write("K\r\n")
                time.sleep(2)  
        except: #-- Si se ha pulsado control-c terminar
            print "Abortando..."
            bd.close()
            break    

Puerto = '/dev/ttyUSB0' #Abro el puerto serie

try:
    s = serial.Serial(Puerto, 9600)
    s.timeout=1;
    # Error al abrir el puerto serie
except serial.SerialException:
    sys.stderr.write("Error al abrir puerto: " + str(Puerto))
    sys.exit(1)
    
print ("Comunicacion establecida con el puerto serie (%s): %s") % (str(Puerto),s.portstr)

# Lanzar el hilo que lee del puerto serie y saca por pantalla
r = threading.Thread(target=reader)
r.start()
   
# Ejecutar el bucle principal. Lee de la consola y envia por el puerto serie
writer()

# Indicar al hilo que termine y esperar
fin=1
r.join()
 
# Cerrar puerto serie.
bd.close()
s.close()
