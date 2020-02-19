
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib.request

import re
#from html.parser import HTMLParser


from urllib.parse import urlsplit

url = "http://www.stallman.org"
base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))  # getting domain name
print(base_url)

#http://ethans_fake_twitter_site.surge.sh/
response = requests.get('http://www.stallman.org')
#response = requests.get('https://en.wikipedia.org/wiki/Polytechnique_Montr%C3%A9al')


soup = str(BeautifulSoup(response.text, 'html.parser'))

pattern = re.compile(r'href="(.*?)"')


matches = pattern.findall(soup)
matches_obj = pattern.finditer(soup)


internal =[]
external = []
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
    print(i)
    try:
        resp = urllib.request.urlopen(i)
        if resp.code == 200:
            print("WORKS")
    except:
        print("ERROR 404!!!")


print("Absolute links")
for i in external:
    print(i)
    try:
        resp = urllib.request.urlopen(i)
        if resp.code == 200:
            print("WORKS")
    except:
        print("ERROR 404!!!")
