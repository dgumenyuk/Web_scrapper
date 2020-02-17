

import requests
from csv import writer
from bs4 import BeautifulSoup
import urllib.request
import re
from html.parser import HTMLParser


#http://ethans_fake_twitter_site.surge.sh/
response = requests.get('https://en.wikipedia.org/wiki/Polytechnique_Montr%C3%A9al')

soup = BeautifulSoup(response.text, 'html.parser')



#print((str(soup)))
p = re.findall('http(.*?)"', str(soup))
#p = re.findall('http.+"', str(soup))

#p = re.findall('(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$', str(soup))
print(len(p))

for i in range(len(p)):
    item = p[i]
    # ... compute some result based on item ...
    item = item + "\n"
    print(item)


                    
