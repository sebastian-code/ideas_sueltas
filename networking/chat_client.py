#!/usr/bin/python
# -*- coding: utf-8 -*-
#######################################################
#						      #
#     Sockets-Chat. Python. Programación Avanzada     #
#	       David López Fernández	      	      #
#	      Ingeniería Informática	              #
#   Ingeniero Técnico en Informática de Sistemas      #
#	       Universidad de Córdoba		      #
#						      #
#######################################################
#Cliente
 
import threading
import socket
 
class escribir(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
	self.mensaje = ''
	self.conn = socket
    def run(self):
	while True:
		self.mensaje = raw_input("Introduce tu mensaje: ")
		self.conn.send(self.mensaje)
	self.conn.close()
 
class leer(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
	self.mensaje = ''
	self.conn = socket
    def run(self):
	while True:
		self.mensaje = self.conn.recv( 1024 )
		print(self.mensaje)
	self.conn.close()
 
miSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
miSocket.connect((socket.gethostname(), 1000))
 
hilos = [escribir(miSocket), leer(miSocket)]
 
for h in hilos:
    h.start()
