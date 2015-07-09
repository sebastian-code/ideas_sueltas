#! /usr/bin/python3
# -*- coding:utf-8 -*-
'''

'''
import platform
import os
import subprocess
import shlex

# uname attributes: system, node, release, version, machine, processor
datos_sistema = platform.uname()


def nom_proc():
    cmd = "cat /proc/cpuinfo | grep 'model name' | head -n 1 | sed 's/model name.*: //g'"
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    temp = process.communicate()[0]
    print(temp)


def vel_proc():
    return str(os.system("cat /proc/cpuinfo | grep 'cpu MHz' | head -n 1 | sed 's/cpu MHz.*: //g'"))


def num_nucleos():
    return str(os.system("cat /proc/cpuinfo | grep 'cpu cores' | head -n 1 | sed 's/cpu MHz.*: //g'"))

'''for i in os.confstr_names:
    if os.confstr(i):
        print(i, os.confstr(i))
'''

'''for i in os.sysconf_names:
    if os.sysconf(i):
        print(i, os.sysconf(i))
'''


def reporte(arg):
    archivo_reporte.write(arg)


def header():
    reporte('''<!DOCTYPE HTML>
<html>
    <head>
        <title>Reporte del Sistema Local Linux</title>
        <style>
            tr > td:first-child { font-weight:bold; }
        </style>
    </head>
    <body>''')


def linea_tabla(arg1, arg2):
    reporte('''
        <tr><td>{0}</td><td>{1}</td></tr>'''.format(arg1, arg2))


def footer():
    reporte('''
    </body>
</html>
    ''')


def informacion_basica():
    reporte('''
        <h2>{}@{}</h2>
        <h3>Configuracion del Sistema</h3>
        <table border=0>'''.format(os.getlogin(), datos_sistema.node))
    linea_tabla('Nombre del Host:', datos_sistema.node)
    linea_tabla('Distribucion:', datos_sistema.version)
    linea_tabla('Kernel:', datos_sistema.release)
    linea_tabla('Arquitectura:', datos_sistema.machine)
    reporte('</table>')


def informacion_hw():
    reporte('''
        <h3>Hardware Overview</h3>
        <h4>Processor</h4>
        <table border=0>''')
    linea_tabla('Nombre del Procesador:', nom_proc)
    linea_tabla('Velocidad del Procesador:', vel_proc)
    linea_tabla('Numero de Nucleos:', num_nucleos)
    linea_tabla('Procesos en Paralelo:', os.cpu_count())
    reporte('</table>')
    reporte('<h4>Graphics</h4>')
    reporte('<table border=0>')

nom_proc()
'''
archivo_reporte = open('sys_report.html', 'a+')

header()
informacion_basica()
informacion_hw()
footer()

archivo_reporte.close()
'''
#################################################################################
'''
hardware_overview() {

  ap ""
  ap ""
  table_row "Model: " "`lspci | grep VGA | sed 's/.*VGA compatible controller://g'`"
  table_row "Driver Module:" "<pre>`lsmod | grep 'fglrx\\|nvidia\\|i915\\|i965\\|intel_agp\\|r200\\|r300\\|r600\\|swrast\\|svga\\|radeon\\|noveau'`</pre>"
  table_row "Tests: " "`glxinfo 2>&1 | grep -i 'direct rendering'`"
  table_row "Display:" "<pre>`xrandr`</pre>"
  ap "</table>"

  ap "<h4>Sound</h4>"
  ap "<table border=0>"
  table_row "Model: " "`lspci | grep Audio | sed 's/.*Audio device://g'`"
  table_row "Driver Module:" "<pre>`lsmod | grep 'snd'`</pre>"
  ap "</table>"

  ap "<h4>Memory</h4>"
  ap "<table border=0>"
  table_row "Memory Total: " "`grep MemTotal /proc/meminfo | sed 's/MemTotal: //g'`"
  table_row "Swap Total: " "`grep SwapTotal /proc/meminfo | sed 's/SwapTotal: //g'`"
  table_row "Swap Free: " "`grep SwapFree /proc/meminfo | sed 's/SwapFree: //g'`"
  ap "</table>"
  ap "<h4>Partitions</h4>\n"
  ap "<pre>`df -h`</pre>"
  ap "<h4>Network</h4>\n"
  ap "<pre>`ifconfig`</pre>"
}

software_overview() {
  ap "<h3>Software Overview</h3>\n"
  ap "<h4>/etc/apt/sources.list</h4>"
  ap "<pre>`cat /etc/apt/sources.list`</pre>"

  ap "<h4>Installed in /opt/GOG Games</h4>\n"
  ap "<pre>`ls -la \"/opt/GOG Games\" 2>&1`</pre>"
  ap "<h4>Installed in /usr/games</h4>\n"
  ap "<pre>`ls -la \"/usr/games\" | grep 'gog-' 2>&1`</pre>"

  ap "<h4>Installed packages</h4>\n"
  ap "<pre>`dpkg-query --show | sed 's/\n/<\/br>/g'`</pre>"
}

modules_overview() {
  ap "<h3>Kernel Modules Overview</h3>\n"
  ap "<h4>lsmod</h4>"
  ap "<pre>`lsmod`</pre>"
}

html_header
basic_information
hardware_overview
modules_overview
software_overview
html_footer

echo -e "${html_output}" > "`xdg-user-dir DESKTOP`/`hostname`_`date +"%H_%M_%d_%m_%Y"`.html"
echo "Done! Your report is in: `xdg-user-dir DESKTOP`/`hostname`_`date +"%H_%M_%d_%m_%Y"`.html"
exit 0
'''
