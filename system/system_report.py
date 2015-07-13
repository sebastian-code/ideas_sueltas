#! /usr/bin/python3
# -*- coding:utf-8 -*-
'''

'''
import platform
import os
import subprocess


# cat /proc/cpuinfo | grep 'model name' | head -n 1 | sed 's/model name.*: //g'
def nom_proc():
    p1 = subprocess.Popen(['cat', '/proc/cpuinfo'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', 'model name'], stdin=p1.stdout,
                          stdout=subprocess.PIPE)
    p3 = subprocess.Popen(['head', '-n 1'], stdin=p2.stdout,
                          stdout=subprocess.PIPE)
    p4 = subprocess.Popen(['sed', 's/model name.*: //g'], stdin=p3.stdout,
                          stdout=subprocess.PIPE)
    p1.stdout.close()
    p2.stdout.close()
    p3.stdout.close()
    return str(p4.communicate()[0])[2:-3]


# cat /proc/cpuinfo | grep 'cpu MHz' | head -n 1 | sed 's/cpu MHz.*: //g'
def vel_proc():
    p1 = subprocess.Popen(['cat', '/proc/cpuinfo'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', 'cpu MHz'], stdin=p1.stdout,
                          stdout=subprocess.PIPE)
    p3 = subprocess.Popen(['head', '-n 1'], stdin=p2.stdout,
                          stdout=subprocess.PIPE)
    p4 = subprocess.Popen(['sed', 's/cpu MHz.*: //g'], stdin=p3.stdout,
                          stdout=subprocess.PIPE)
    p1.stdout.close()
    p2.stdout.close()
    p3.stdout.close()
    return str(p4.communicate()[0])[2:-3]


# cat /proc/cpuinfo | grep 'cpu cores' | head -n 1 | sed 's/cpu MHz.*: //g'
def num_nucleos():
    p1 = subprocess.Popen(['cat', '/proc/cpuinfo'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', 'cpu cores'], stdin=p1.stdout,
                          stdout=subprocess.PIPE)
    p3 = subprocess.Popen(['head', '-n 1'], stdin=p2.stdout,
                          stdout=subprocess.PIPE)
    p4 = subprocess.Popen(['sed', 's/cpu cores.*: //g'], stdin=p3.stdout,
                          stdout=subprocess.PIPE)
    p1.stdout.close()
    p2.stdout.close()
    p3.stdout.close()
    return str(p4.communicate()[0])[2:-3]


# lspci | grep VGA | sed 's/.*VGA compatible controller://g'
def vga_modelo():
    p1 = subprocess.Popen('lspci', stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', 'VGA'], stdin=p1.stdout,
                          stdout=subprocess.PIPE)
    p3 = subprocess.Popen(['sed', 's/.*VGA compatible controller://g'],
                          stdin=p2.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    p2.stdout.close()
    return str(p3.communicate()[0])[3:-12]


# lsmod | grep 'fglrx | nvidia | i915 | i965 | intel_agp | r200 | r300 | r600 | swrast | svga | radeon | noveau'
def vga_driver():
    p1 = subprocess.Popen('lsmod', stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', 'fglrx\\|nvidia\\|i915\\|i965\\|intel_agp\\|r200\\|r300\\|r600\\|swrast\\|svga\\|radeon\\|noveau'],
                          stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    st = str(p2.communicate()[0])[2:-3].replace('\\n', '<br />')
    return st


# glxinfo 2>&1 | grep -i 'direct rendering'
def vga_rendering():
    p1 = subprocess.Popen(['glxinfo'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', '-i', 'direct rendering'],
                          stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    return str(p2.communicate()[0])[2:-3]


# xrandr
def vga_displays():
    p1 = subprocess.Popen('xrandr', stdout=subprocess.PIPE)
    st = str(p1.communicate()[0])[2:-3].replace('\\n', '<br />')
    return st


# lspci | grep Audio | sed 's/.*Audio device://g'
def snd_modelo():
    p1 = subprocess.Popen('lspci', stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', 'Audio'], stdin=p1.stdout,
                          stdout=subprocess.PIPE)
    p3 = subprocess.Popen(['sed', 's/.*Audio device://g'],
                          stdin=p2.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    p2.stdout.close()
    return str(p3.communicate()[0])[3:-3]


# lsmod | grep 'snd'
def snd_driver():
    p1 = subprocess.Popen('lsmod', stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', 'snd'],
                          stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    st = str(p2.communicate()[0])[2:-3].replace('\\n', '<br />')
    return st

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
        <table border=0>'''.format(os.getlogin(), platform.node()))
    linea_tabla('Nombre del Host:', platform.node())
    linea_tabla('Distribucion:', (platform.linux_distribution()[0],
                                  platform.linux_distribution()[1]))
    linea_tabla('Kernel:', platform.release())
    linea_tabla('Arquitectura:', platform.machine())
    reporte('</table>')


def informacion_cpu():
    reporte('''
        <h3>Configuracion de Hardware</h3>
        <h4>Procesador</h4>
        <table border=0>''')
    linea_tabla('Nombre del Procesador:', nom_proc())
    linea_tabla('Velocidad del Procesador:', vel_proc())
    linea_tabla('Numero de Nucleos:', num_nucleos())
    linea_tabla('Procesos en Paralelo:', os.cpu_count())
    reporte('</table>')


def informacion_graph():
    reporte('''
        <h4>Graphics</h4>
        <table border=0>
    ''')
    linea_tabla('Modelo:', vga_modelo())
    linea_tabla('Driver:', '''<pre>{}</pre>'''.format(vga_driver()))
    linea_tabla('Rendering:', vga_rendering())
    linea_tabla('Displays:', '<pre>{}</pre>'.format(vga_displays()))
    reporte('</table>')


def informacion_snd():
    reporte('''
        <h4>Sound</h4>
        <table border=0
    ''')
    linea_tabla('Modelo:', snd_modelo())
    linea_tabla('Driver:', '<pre>{}</pre>'.format(snd_driver()))
    reporte('</table>')

if __name__ == '__main__':
    archivo_reporte = open('sys_report.html', 'a+')
    header()
    informacion_basica()
    informacion_cpu()
    informacion_graph()
    informacion_snd()
    footer()
    archivo_reporte.close()


'''
for i in os.confstr_names:
    if os.confstr(i):
        print(i, os.confstr(i))


for i in os.sysconf_names:
    if os.sysconf(i):
        print(i, os.sysconf(i))
'''
#################################################################################
'''

  ap "<h4>Memory</h4>"
  ap "<table border=0>"
  table_row "Memory Total: " "`grep MemTotal /proc/meminfo | sed 's/MemTotal: //g'`"
  table_row "Memory Free: " "`grep MemFree /proc/meminfo | sed 's/MemFree: //g'`"
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
