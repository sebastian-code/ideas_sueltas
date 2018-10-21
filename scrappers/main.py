from general import create_dir, write_file
from domain_name import get_domain_name
from ip_address import get_ip_address
from nmap import get_nmap
from robots_txt import get_robots_txt
from whois import who_is


ROOT_DIR = "companies"
create_dir(ROOT_DIR)
def gather_info(name, url):
    robots_txt = get_robots_txt(url)
    domain = get_domain_name(url)
    whois = who_is(domain)
    ipaddress = get_ip_address(domain)
