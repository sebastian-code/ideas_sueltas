#! /usr/bin/python3
# -*- coding:utf-8 -*-
'''

'''
html_output = ""
GOG_SYSTEM_REPORT_VERSION = "1.1"
ap() {
  html_output=$html_output$1
}

table_row() {
  ap "<tr><td>${1}</td><td>${2}</td></tr>"
}

html_style() {
  ap "<style>\n"
  ap "tr > td:first-child { font-weight:bold; }"
  ap "</style>\n"
}

html_header() {
  ap "<html>\n<head>"
  ap "<title>"$USER"@"`hostname`"</title>"
  html_style
  ap "</head>\n<body>"
}

html_footer() {
  ap "\n</body>\n</html>"
}

basic_information() {
  ap "<h2>"`hostname`"</h2>"
  ap "GOG.com System Report: ${GOG_SYSTEM_REPORT_VERSION}"
  ap "<h3>System Configuration</h3>\n"
  ap "<table border=0>"
  table_row "Hostname:" `hostname`
  distro=`lsb_release -sd`
  table_row "Distribution:" "${distro}"
  table_row "Kernel: " "`uname --kernel-release`"
  table_row "Architecture: " `uname -m`
  ap "</table>"
}

hardware_overview() {
  ap "<h3>Hardware Overview</h3>\n"
  ap "<h4>Processor</h4>\n"
  ap "<table border=0>"
  table_row "Processor Name:" "`cat /proc/cpuinfo | grep "model name" | head -n 1 | sed 's/model name.*: //g'`"
  table_row "Processor Speed:" "`cat /proc/cpuinfo | grep "cpu MHz" | head -n 1 | sed 's/cpu MHz.*: //g'`"
  table_row "Processor Cores:" `cat /proc/cpuinfo | grep "cpu cores" | head -n 1 | sed 's/cpu cores.*: //g'`
  ap "</table>"

  ap "<h4>Graphics</h4>"
  ap "<table border=0>"
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
