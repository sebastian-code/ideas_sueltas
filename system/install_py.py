#! /usr/bin/python
# -*- coding:utf-8 -*

'''
Created on 16/01/2014
@summary: Script generico para el despliegue de software en diferentes modalidades.
@author: Sebastian Reyes Espinosa.
@contact: sebaslander@gmail.com
@organization: Técnica Humana S.A.S.
@version: v0.1
'''

import os, sys, argparse

def str_install():
    validate_py()
    is_deb, is_rpm = validate_os()
    if is_deb:
        install_deb()
    if is_rpm:
        install_rpm()

def validate_os():

    import platform

    os = platform.system()
    if os == 'Linux':
        distro = platform.linux_distribution()[0].lower().replace('"', '')
        is_rpm = distro in ("redhat", "red hat enterprise linux server", "centos", "centos linux", "fedora")
        is_deb = distro in ("debian", "ubuntu", "elementary os", "linuxmint")
        print 'Su sistema operativo es %s... invocando el instalador correspondiente' % os
        print 'Su distribucion es %s... verificando disponibilidad de instaladores' % distro
        if not (is_deb or is_rpm):
            print 'Este instalador solo funciona con administradores de paquetes RPM y DEB'
            print 'Este instalador se cerrara por un error de reconocimiento de su distro.'
            print 'Por favor, verifique las condiciones de su distro e intente correr el'
            print 'instalador nuevamente.'
            sys.exit(1)
        else:
            return is_deb, is_rpm
    else:
        print('''Este instalador solo es adecuado para despliegues de la
        plataforma en entornos Linux, el instalador se cerrara por un error de
        incompatibilidad con su sistema operativo.

        Por favor, verifique las condiciones de su sistema operativo e intente
        correr el instalador nuevamente.
        ''')
        sys.exit(1)


def validate_py():
    py_ver = sys.version[:5]
    print "Python Version =", py_ver
    if py_ver[:3] == '2.7':
        print 'Su version de Python es correcta y se puede continuar con la instalacion.'
        return
    else:
        print 'Su version de Python es incompatible con la plataforma.'
        print 'Actualmente usted tiene instalado', py_ver, 'y para correr el'
        print 'instalador, se requiere que se tenga instalada la version'
        print '2.7+ de Python'
        print ''
        sys.exit(1)


def install_deb():
    pass


def install_rpm():
    pass


def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    validate_py()
