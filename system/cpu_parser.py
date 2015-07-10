#! /usr/bin/python3
# -*- coding:utf-8 -*-

""" print out the /proc/cpuinfo
    file
"""

with open('/proc/cpuinfo') as f:
    for line in f:
        print(line.rstrip('\n'))



""" Print the model of your processing units
"""
with open('/proc/cpuinfo') as f:
    for line in f:
        # Ignore the blank line separating the information between
        # details about two processing units
        if line.strip():
            if line.rstrip('\n').startswith('model name'):
                model_name = line.rstrip('\n').split(':')[1]
                print(model_name)



""" Find the real bit architecture
"""

with open('/proc/cpuinfo') as f:
    for line in f:
        # Ignore the blank line separating the information between
        # details about two processing units
        if line.strip():
            if line.rstrip('\n').startswith('flags') \
                    or line.rstrip('\n').startswith('Features'):
                if 'lm' in line.rstrip('\n').split():
                    print('64-bit')
                else:
                    print('32-bit')



"""
/proc/cpuinfo as a Python dict
"""

from collections import OrderedDict
import pprint

def cpuinfo():
    ''' Return the information in /proc/cpuinfo
    as a dictionary in the following format:
    cpu_info['proc0']={...}
    cpu_info['proc1']={...}

    '''

    cpuinfo=OrderedDict()
    procinfo=OrderedDict()

    nprocs = 0
    with open('/proc/cpuinfo') as f:
        for line in f:
            if not line.strip():
                # end of one processor
                cpuinfo['proc%s' % nprocs] = procinfo
                nprocs=nprocs+1
                # Reset
                procinfo=OrderedDict()
            else:
                if len(line.split(':')) == 2:
                    procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
                else:
                    procinfo[line.split(':')[0].strip()] = ''

    return cpuinfo

if __name__=='__main__':
    cpuinfo = cpuinfo()
    for processor in cpuinfo.keys():
        print(cpuinfo[processor]['model name'])
