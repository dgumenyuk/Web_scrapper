
import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib.request
import re
from urllib.error import URLError, HTTPError
from urllib.parse import urlsplit
import colorama


colorama.init()
green = colorama.Fore.GREEN
yellow = colorama.Fore.YELLOW
gray = colorama.Fore.LIGHTBLACK_EX
red = colorama.Fore.RED
white = colorama.Fore.WHITE
reset = colorama.Fore.RESET

url = "http://www.stallman.org"

base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))  # getting domain name
print("Base URL: ")
print(base_url)

response = requests.get('http://www.stallman.org')

soup = str(BeautifulSoup(response.text, 'html.parser'))

pattern = re.compile(r'href="(.*?)"')

matches = pattern.findall(soup)
matches_obj = pattern.finditer(soup)

internal = []
external = []
all_ = []
broken_links = []
plain_text = []

for element in matches:
    if element[0:4] == "http":
        external.append(element)
        all_.append(element)
    else:
        element = urljoin(base_url, element)
        internal.append(element)
        all_.append(element)
        

print(white + "Relative links:")
for i in internal:
    print("Link: ")
    print(yellow + i)
    try:
        resp = urllib.request.urlopen(i, timeout=10)
        if resp.code == 200:
            print(green + "WORKS")
            print("\n")
    except HTTPError as e:
        print(red + "DOES NOT WORK")
        print(red + 'The server couldn\'t fulfill the request.')
        print(red + 'Error code: ', e.code)
        print("\n")
    except URLError as e:
        print(red + 'We failed to reach a server.')
        print(red + 'Reason: ', e.reason)
        print("\n")


print(white + "Absolute links:")
for i in external:
    print("Link: ")
    print(yellow + i)
    try:
        resp = urllib.request.urlopen(i, timeout=10)
        if resp.code == 200:
            print(green + "WORKS")
            print("\n")
    except HTTPError as e:
        print(red + "DOES NOT WORK")
        print(red + 'The server couldn\'t fulfill the request.')
        print(red + 'Error code: ', e.code)
        print("\n")
    except URLError as e:
        print(red + 'We failed to reach a server.')
        print(red + 'Reason: ', e.reason)
        print("\n")
       

pattern = re.compile(r' http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+[ .]')
matches = pattern.findall(soup)

for element in matches:
    # if not(element in all_):
    if element not in all_:
        plain_text.append(element)

print(white + "Plain text links:")

for i in plain_text:
    print("Link: ")
    print(yellow + i)
    try:
        resp = urllib.request.urlopen(i, timeout=10)
        print(green + "WORKS")
        print("\n")
    except HTTPError as e:
        print(red + "DOES NOT WORK")
        print(red + 'The server couldn\'t fulfill the request.')
        print(red + 'Error code: ', e.code)
        print("\n")
