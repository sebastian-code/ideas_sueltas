import os


def who_is(url):
    command = os.popen(f"whois {url}")
    return str(command.read())
