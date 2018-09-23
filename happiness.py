#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Pieza original para lograr el diccionario sin tanto trabajo, pero tambien para
probar otra aproximacion.

nums = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
        21, 22, 23, 24, 25, 26)
letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
           'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')

dic = {}

for v in nums:
    dic[letters[v - 1]] = v

print(sorted(dic.items()))
"""

dicc = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8,
        'i': 9, 'j': 10, 'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15,
        'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20, 'u': 21, 'v': 22,
        'w': 23, 'x': 24, 'y': 25, 'z': 26}

fword = 'knowledge'
sword = 'hardwork'
tword = 'attitude'
frest = 0
srest = 0
trest = 0

for i in fword:
    frest += dicc[i]

for i in sword:
    srest += dicc[i]

for i in tword:
    trest += dicc[i]

print('The path to succes:\n')
print(fword + ' Value: ' + str(frest) + '%')
print(sword + ' Value: ' + str(srest) + '%')
print(tword + ' Value: ' + str(trest) + '%')
