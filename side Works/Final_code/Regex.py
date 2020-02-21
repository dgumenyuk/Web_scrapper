
import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib.request
import re
from urllib.error import URLError, HTTPError

import colorama


colorama.init()
green = colorama.Fore.GREEN
yellow = colorama.Fore.YELLOW
gray = colorama.Fore.LIGHTBLACK_EX
red = colorama.Fore.RED
reset = colorama.Fore.RESET


from urllib.parse import urlsplit

url = "http://www.stallman.org"

base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))  # getting domain name
print(base_url)

#http://ethans_fake_twitter_site.surge.sh/
response = requests.get('http://www.stallman.org')
#response = requests.get('https://en.wikipedia.org/wiki/Polytechnique_Montr%C3%A9al')


soup = str(BeautifulSoup(response.text, 'html.parser'))



Plain_TEXT_Link = []
for Nelement in soup.split():
	if ("http" or "https") in Nelement and ("href") not in Nelement:
		Plain_TEXT_Link.append(Nelement)


pattern = re.compile(r'href="(.*?)"')


matches = pattern.findall(soup)
matches_obj = pattern.finditer(soup)
# for element in matches_obj:
#     print(element.pos)
    
internal =[]
external = []
broken_links = []
for element in matches:
    #if ("http://" or "https://") in element:
    #if element.find('http', 0, 5):
    if element[0:4] == "http":
    
        external.append(element)
    else:
        element =urljoin(base_url, element)
        #element = urljoin("element")
        internal.append(element)

print("Relative links")
for i in internal:
    print(yellow + i)
    try:
        resp = urllib.request.urlopen(i)
        if resp.code == 200:
            print(green + "WORKS")
    except HTTPError as e:
        print(red + 'The server couldn\'t fulfill the request.')
        print(red + 'Error code: ', e.code)
    except URLError as e:
        print(red + 'We failed to reach a server.')
        print(red + 'Reason: ', e.reason)


print("Absolute links")
for i in external:
    print(i)
    try:
        resp = urllib.request.urlopen(i)
        if resp.code == 200:
            print(green + "WORKS")
    except HTTPError as e:
        print(red + 'The server couldn\'t fulfill the request.')
        print(red + 'Error code: ', e.code)
    except URLError as e:
        print(red + 'We failed to reach a server.')
        print(red + 'Reason: ', e.reason)
