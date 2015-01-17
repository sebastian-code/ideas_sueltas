# -*- coding:utf-8 -*
#!/usr/bin/env python

from threading import Thread
from multiprocessing import Process

def do_run():
    a, b = 0, 1
    for i in range(1000000):
        a, b = b, a * b

class normal(object):
    def run(self):
        do_run()

class hilos(Thread):
    def run(self):
        do_run()

class procesos(Process):
    def run(self):
        do_run()

def ejecuta(iteraciones, tipo):  
    funcs = list()
    if tipo == 'normal':
      t_object = normal

    elif tipo == 'hilos':
      t_object = hilos

    else:
      t_object = procesos

    for i in range(int(iteraciones)):
        funcs.append(t_object())

    if tipo == 'normal':
      for i in funcs:
	    i.run()

    else:      
      for i in funcs:
        i.start()

      for i in funcs:
        i.join()

def print_results(func, results):
    print "%-23s %4.6f segundos" % (func, results)

if __name__ == 'main':
    import sys
    from timeit import Timer    
    if len(sys.argv) < 2:
        print 'Uso: %s nombre_test\n' % sys.argv0
        sys.exit(1)

    test_name = sys.argv1
    if test_name.endswith('.py'):
        test_name = test_name[:-3]

    print 'Cargando test %s' % test_name
    test = import(test_name)
    do_run = test.do_run
    print 'Lanzando test…'
    for i in range(1, 11):
	if i not in [1, 2, 6, 10]:
	  continue
        t = Timer('ejecuta(%s, 'normal’)' % i, 'from main import ejecuta')
        #br = min(t.repeat(repeat=100, number=1))        
        br = sum(t.repeat(repeat=100, number=1))        
        print_results('normal (%s iteraciones)' % i, br)
        t = Timer('ejecuta(%s, 'hilos’)' % i, 'from main import ejecuta')
        br = sum(t.repeat(repeat=100, number=1))
        print_results('hilos (%s hilos)' % i, br)
        t = Timer('ejecuta(%s, 'procesos’)' % i, 'from main import ejecuta')
        br = sum(t.repeat(repeat=100, number=1))
        print_results('pocesos (%s procesos)' % i, br)
        print '\n',

    print 'Test completado'
