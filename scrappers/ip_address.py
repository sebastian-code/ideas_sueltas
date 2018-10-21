import os


def get_ip_address(url):
    results = str(os.popen(f"host {url}"))
    marker = results.find("has address") + 12
    return results[marker:].splitlines()[0]
