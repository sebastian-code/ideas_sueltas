import os


def get_nmap(options, ip):
    process = os.popen(f"nmap {options} {ip}")
    return  str(process.read())
