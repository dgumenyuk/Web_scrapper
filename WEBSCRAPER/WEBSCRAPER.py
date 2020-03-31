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
cyan = colorama.Fore.CYAN
gray = colorama.Fore.LIGHTBLACK_EX
red = colorama.Fore.RED
yellow = colorama.Fore.YELLOW
magneta = colorama.Fore.MAGENTA
reset = colorama.Fore.RESET

internal_url = set()
external_url = set()
plainText_url = set()
broken_url = set()

count = 0

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

        if not valild(element):               # check the validity of the link
            continue

        if element in internal_url:
            continue

        if base_url not in element:              # correction of prior script in order to reduce the duplication and check the external link without browsing them
            if element not in external_url:
                check(element)
                external_url.add(element)
            continue

        check(element)                # check the internal link
        urls.add(element)             # create urls to have the internal urls to crawl and browse them
        internal_url.add(element)     # internal_link to have the number of the internal links and prevent from duplication
        global count
        count += 1

        print(count)

    return urls
        # if element[0:4] == "http":
        #     ALLURLS.add(element)
        #     if is_valild(element):
        #         external_url.add(element)
        #         print(cyan + "External link")
        #         check(element)
        #
        # else:                                    # finding internal_url links
        #     element = urljoin(base_url, element)
        #     ALLURLS.add(element)
        #     if is_valild(element):
        #         internal_url.add(element)
        #         print(cyan + "Internal link")
        #         check(element)


    # pattern = re.compile(r' http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+[ .]')  # regex that finds all URLs in the plain text
    # matches = pattern.findall(soup)
    #
    # for element in matches:
    #     if element not in ALLURLS:
    #           # make sure it was not in internal or external links, then it must be in plain text
    #         plainText_url.add(element)
    #         print(cyan + "Plain text link")
    #         check(element)

# def crawler(url):
#     links = link_extractor(url)
#     for link in links:
#         crawler(link)


if __name__ == "__main__":                             # main class to do the process


    URL = input("Please enter a url: ")
    crawler(URL)

    print("=========================================================================================================")
    print(gray + "Total number of the valid links = ", len(internal_url) + len(external_url) + len(plainText_url))
    print(gray + "Total number of the valid internal_url links = ", len(internal_url))
    print(gray + "Total number of the valid external_url links = ", len(external_url))
    print(gray + "Total number of the valid links in the body text = ", len(plainText_url))
    print("=========================================================================================================")
    print(yellow + "Total number of the dead links (forbidden, not found, inaccessible) are ", len(broken_url))
