#! /usr/bin/python2.7
# -*- coding:utf-8 -*-

"""
Created on 2014/12/05
@note: Ping Test
@note: Compatible unicamente con Python 2.7+
@summary: Siempre hace falta tener un buen script que permita hacer de forma
		  menos manual en los momentos en que se tienen muchas direcciones IP.
@contact: info@catalisys.com
@organization: Catalisys S.A.S.
@updated: 2014/07/19
@version: v2.0.01
"""

from threading import Thread
import subprocess
from Queue import Queue

num_threads = 4
queue = Queue()
ips = ["192.168.3.135", "192.168.3.136", "192.168.3.137", "192.168.3.138",
       "192.168.3.139", "192.168.3.140", "192.168.3.141", "192.168.3.142", 
       "192.168.3.143", "192.168.3.144", "192.168.3.145", "192.168.3.146",
       "192.168.3.147", "192.168.3.148", "192.168.3.149", "192.168.3.150", 
       "192.168.3.151", "192.168.3.152", "192.168.3.153", "192.168.3.154", 
       "192.168.3.155"]
#wraps system ping command
def pinger(i, q):
    """Pings subnet"""
    while True:
        ip = q.get()
        print "Thread %s: Pinging %s" % (i, ip)
        ret = subprocess.call("ping -c 1 %s" % ip, shell=True, 
                        stdout=open('tes.txt', 'w'), stderr=subprocess.STDOUT)
        if ret == 0:
            print "%s: is alive" % ip
        else:
            print "%s: did not respond" % ip
        q.task_done()
#Spawn thread pool
for i in range(num_threads):

    worker = Thread(target=pinger, args=(i, queue))
    worker.setDaemon(True)
    worker.start()
#Place work in queue
for ip in ips:
    queue.put(ip)
#Wait until worker threads are done to exit    
queue.join()
