import io
import urllib.request


def get_robots_txt(url):
    if not url.endswith("/"):
        path = url + "/"


    request = urllib.request.urlopen(f"{path}robots.txt", data=None)
    data = io.TextIOWrapper(request, encoding="utf-8")
    return data.read()
