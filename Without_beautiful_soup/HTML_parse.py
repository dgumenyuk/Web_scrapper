
import urllib.request

from html.parser import HTMLParser

class MyParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a':
             for attr in attrs:
                 if attr[0]=='href':
                     absolute=urllib.request.urljoin(self.url, attr[1])
                     if absolute[:7]=='http://':
                         self.https.append(absolute)


def getWebInfo(url):
    infile=urllib.request.urlopen(url)
    content=infile.read().decode()
    infile.close()
    https=[]

    parser=MyParser()
    parser.https = https
    parser.url = url
    parser.feed(content)

    print('ALL ABSOLUTE LINKS ON THE WEB PAGE')
    print('--------------------------------------')
    return https

links = getWebInfo('http://www.ianbicking.org/blog/2008/03/python-html-parser-performance.html')


for link in links:
    print(link)

