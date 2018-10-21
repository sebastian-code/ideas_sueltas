'''
Created on 8/09/2013
@author: Sebastian Reyes Espinosa
@version: 0.1

'''
#!/usr/bin/python
'''
import sys
arg = len(sys.argv)
if arg == 1:
    print 'Modo de uso: Romanos.py numero_romano'
    sys.exit(1)
'''
roma = {'M': 1000, 'D':500, 'C':100, 'L':50, 'X':10, 'V':5, 'I':1}
# romano = sys.argv[1].upper()
romano = raw_input("Introduzca un Numero Romano: ").upper()
letras = list(romano)
resultado = 0
anterior = 0
for letra in letras:
    if letra in roma:
        if roma[letra] > anterior:
            resultado = resultado - anterior * 2
            resultado = resultado + roma[letra]
        else:
            resultado = resultado + roma[letra]
            anterior = roma[letra]
    else:
        print 'Letras desconocidas'
#        sys.exit(2)
print resultado