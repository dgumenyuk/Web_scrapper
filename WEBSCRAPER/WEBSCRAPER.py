"""
This is a program to find  broken links of the website.
It gives the total number of links, number of internal, external, plain text and broken links.

Source:
https://github.com/dgumenyuk/Web_scrapper/tree/master/WEBSCRAPER

"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import urllib.request
import re
from urllib.error import URLError, HTTPError
from urllib.parse import urlsplit
import colorama

colorama.init()
green = colorama.Fore.GREEN
blue = colorama.Fore.BLUE
cyan = colorama.Fore.CYAN
gray = colorama.Fore.LIGHTBLACK_EX
red = colorama.Fore.RED
yellow = colorama.Fore.YELLOW
magneta = colorama.Fore.MAGENTA
white = colorama.Fore.WHITE
reset = colorama.Fore.RESET

internal_url = set()
external_url = set()
plainText_url = set()
broken_url = set()

def check(url):         # check the url in order to find the broken links

    try:
        resp = urllib.request.urlopen(url, timeout=10)
        if resp.code == 200:
            print(green + url + "\nisn't broken")
            print("\n")
    except HTTPError as e:  # execute if the error occured
        print(red + url + "\nis broken" + "\nWe failed to reach a server for the: " + url)
        print(red + 'Error code: ', e.code)
        print("\n")

    except URLError as e:
        print(red + url + "\nis broken" + "\nWe failed to reach a server for the: " + url)
        print(red + 'Reason: ', e.reason)
        print("\n")


def valild(url):        # check the validity of the url using the url protocol and the domain
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def link_extractor(url):          # crawl the webSite (url) to extract all the available links
    urls = set()
    response = requests.get(url)
    soup = str(BeautifulSoup(response.text, 'html.parser'))  # get the html page as a string
    base_url = urlparse(url).netloc  # get the base URL (domain)

    pattern = re.compile(r'href="(.*?)"')
    matches = pattern.findall(soup)

    for element in matches:
        element = urljoin(url, element)

        if " " in element:  #this condition is just added in order to prevent from a bad link. (an example in the http://swat.polymtl.ca/index.html)
            continue

        if not valild(element):               # check the validity of the link
            continue

        if element in internal_url:
            continue

        if base_url not in element:              # correction of prior script in order to reduce the duplication and check the external link without browsing them
            if element not in external_url:
                print(cyan + "External Link")
                check(element)
                external_url.add(element)
            continue

        print(cyan + "Internal Link")
        check(element)                # check the internal link
        urls.add(element)             # create urls to have the internal urls to crawl and browse them
        internal_url.add(element)     # internal_link to have the number of the internal links and prevent from duplication

    pattern = re.compile(r' http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+[ .]')  # regex that finds all URLs in the plain text
    matches = pattern.findall(soup)

    for element in matches:
        element = urljoin(url, element)
        print(element)

        if " " in element:
            continue

        if not valid(element):
            continue
                                                # same as the actions for the internal and external links
        if element in internal_url:
            continue

        if element in external_url:
            continue

        if base_url not in element:
            if element not in plainText_url:
                print(cyan + "Plain Text Link")
                check(element)
                plainText_url.add(element)

    return urls


def crawler(url):                        # the crawler function crawls the websites using their internal links
    links = link_extractor(url)
    for link in links:
        crawler(link)



if __name__ == "__main__":                             # main class to do the process

    Specifier = ''
    conditionsFileType = ('1', '2', '3')

    CrawlingActivation = ''
    conditionsCrawling = ('Y', 'N')

    while Specifier not in conditionsFileType:
        Specifier = input(white + "Please specify the type of input method you want to use:\n\n1.a URL (html web page)\n2.a file containing list of urls (a .txt or .csv file)\n3.a list of website file (directories containing unlaunched websites files)\n\nPlease select one of the above options: [1/2/3] ")
    if int(Specifier) == 1:
        URL = input("\nPlease enter a url: ")
        while CrawlingActivation.upper() not in conditionsCrawling:
            CrawlingActivation = input("\n" + white + "Do you want to keep the " + blue + "CRAWLING" + white + " Activated? [Y/n]  ")
        CrawlingActivation = CrawlingActivation.upper()
        if CrawlingActivation == ("Y"):
            crawler(URL)
        if CrawlingActivation == ("N"):
            link_extractor(URL)


    # if int(Specifier) == 2:
    #     URL = input("\nPlease enter the address of the file (.txt or .csv) containing list of the urls: ")
    #     while CrawlingActivation.upper() not in conditionsCrawling:
    #         CrawlingActivation = input("\n" + white + "Do you want to keep the " + blue + "CRAWLING" + white + " Activated? [Y/n]  ")
    #     CrawlingActivation = CrawlingActivation.upper()
    #     if CrawlingActivation == ("Y"):
    #         crawler(URL)
    #     if CrawlingActivation == ("N"):
    #         link_extractor(URL)
    #
    # if int(Specifier) == 3:
    #     print("\nPlease be aware in this situatuion the Crawling is deactivated")
    #     URL = input("\nPlease enter the address of the file containing unlaunched wesites: ")
    #     link_extractor(URL)



    print("=========================================================================================================")
    print(gray + "Total number of the valid links = ", len(internal_url) + len(external_url) + len(plainText_url))
    print(gray + "Total number of the valid internal_url links = ", len(internal_url))
    print(gray + "Total number of the valid external_url links = ", len(external_url))
    print(gray + "Total number of the valid links in the body text = ", len(plainText_url))
    print("=========================================================================================================")
    print(yellow + "Total number of the dead links (forbidden, not found, inaccessible) are ", len(broken_url))
