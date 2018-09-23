#! /usr/bin/python
# -*- coding:utf-8 -*-
'''
Created on 28/11/2013
@note: Archivo de arranque para aplicacion de gestion de contactos con interfaz grafica.
@summary: Miniterminal de comunicaciones puerto serial.
@author: Sebastian Reyes Espinosa.
@organization: Técnica Humana S.A.S. 
@version: v0.5
@updated: 05/12/2013
'''

import sys
import getopt
import serial
import consola_io
import threading
import time
from datetime import datetime
 
# Caracter empleado para salir del terminal
salida = '\x04'   #ctrl+D
 
# Variable para indicar al thread que termine
fin = 0

# Este hilo se ejecuta infinitamente. Lee datos del puerto serie y sacandolos por la consola

def reader():
    while not(fin):
        try:
            data = s.read()
            #h = str(datetime.now())
            sys.stdout.write(data)
            sys.stdout.flush()
            bd = open("salida.txt", "a")
            #bd.write(h + '-' + data)
            bd.write(data)
            bd.flush()
            #bd.write("\n")
            
        except:
            print "Excepcion: Abortando..."
            bd.close()
            break;       
 
# Este es el bucle principal. Todos los caracteres que llegan por la consola se envian por el puerto serie

def writer():
    while 1:
        try:
            '''
            # Esperar a que se pulse una tecla
            c = consola_io.getkey()
            # Si es la tecla de fin se termina
            if c == salida:
                break
            
            else:
                # Enviar tecla por el puerto serie
                s.write("K\r\n")
            '''
            while 1:
                s.write("K\r\n")
                time.sleep(2)  
        except: #-- Si se ha pulsado control-c terminar
            print "Abortando..."
            break    
 
 
# Imprimir mensaje de ayuda

def ayuda():
    sys.stderr.write("""Uso: miniterm [opciones]
    Miniterminal de comunicaciones en python
    opciones:
    -p, --port=PORT: Puerto serie a emplear. Bien un numero o una cadena
    
    Ejemplo:
    terminalita -p 0    --> Usar el primer puerto serie (Linux/Windos)
    terminalita -p /dev/ttyS1 --> Especificar el dispositivo serie (Linux)
    """)

# Analizar los argumentos pasados por el usuario

def Analizar_argumentos():
    # Valor por defecto del puerto a usar
    Puerto = '/dev/ttyUSB0'
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hp:",["help", "port="])

    except getopt.GetoptError:
        # Imprimir informacion de ayuda y terminar ejecucion:
        ayuda()
        sys.exit(2)
    
    # Leer argumentos pasados
    for o, a in opts:
        if o in ("-h", "--help"):
            ayuda()
            sys.exit()
        elif o in ("-p", "--port"): #specified port
            try:
                Puerto = int(a)
                
            except ValueError:
                Puerto = a
                
    return Puerto
 
# Bloque principal
# Funcion = Analizar los argumentos pasados por el usuario

Puerto=Analizar_argumentos()
 
#Abrir el puerto serie
try:
    s = serial.Serial(Puerto, 9600)
    #-- Timeout: 1 seg
    s.timeout=1;

except serial.SerialException:
    # Error al abrir el puerto serie
    sys.stderr.write("Error al abrir puerto: " + str(Puerto))
    sys.exit(1)
    
print ("Puerto serie (%s): %s") % (str(Puerto),s.portstr)
print ("--- Miniterm --- Ctrl-D para terminar\n")

# Lanzar el hilo que lee del puerto serie y saca por pantalla
r = threading.Thread(target=reader)
r.start()
   
# Ejecutar el bucle principal. Lee de la consola y envia por el puerto serie
writer()

# Indicar al hilo the termine y esperar
fin=1
r.join()
 
# Fin del programa
print "\n"
print "--- Fin ---"
 
# Cerrar puerto serie.
s.close()
