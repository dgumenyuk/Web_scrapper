

import requests
from csv import writer
from bs4 import BeautifulSoup
import urllib.request
import re
from html.parser import HTMLParser


#http://ethans_fake_twitter_site.surge.sh/
#response = requests.get('http://www.stallman.org')
response = requests.get('https://en.wikipedia.org/wiki/Polytechnique_Montr%C3%A9al')


soup = str(BeautifulSoup(response.text, 'html.parser'))

'''

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
'''

#pattern = re.compile(r'="[a-zA-Z]*(://)(www\.)?\w+\.\w+')
pattern = re.compile(r'href="(.*?)"')

#pattern = re.compile(r'(http:\/)?(\/[\w\.\-]+)+\/?')

matches = pattern.findall(soup)
matches_obj = pattern.finditer(soup)
result = ""
end = 'w'
i = 0
#for (match, match_obj) in zip(matches, matches_obj):
    #print(match)
    

#print(result)
#[a-zA-Z0-9.]*"')


internal =[]
external = []
for element in matches:
    #if ("http://" or "https://") in element:
    #if element.find('http', 0, 5):
    if element[0:4] == "http":
    
        external.append(element)
    else:
        internal.append(element)
        
for i in external:
    print(i)
    
        
