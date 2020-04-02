"""
This is a program to find  broken links of the website.
It gives the total number of links, number of internal, external, plain text and broken links.

Source:
https://github.com/dgumenyuk/Web_scrapper/tree/master/WEBSCRAPER

"""
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import urllib.request
import re
from urllib.error import URLError, HTTPError
from urllib.parse import urlsplit
import colorama
import os

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

regex = re.compile(r'^(?:http|ftp)s?://' # http:// or https://                                                        #regex in order to find the http[s] url
                   r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                   r'localhost|' #localhost...
                   r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                   r'(?::\d+)?' # optional port
                   r'(?:/?|[/?]\S+)$', re.IGNORECASE)

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
        broken_url.add(url)

    except URLError as e:
        print(red + url + "\nis broken" + "\nWe failed to reach a server for the: " + url)
        print(red + 'Reason: ', e.reason)
        print("\n")
        broken_url.add(url)


def valild(url):        # check the validity of the url using the url protocol and the domain
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def URL_link_extractor(url):          # scrape the webSite (url) to extract all the available links

    response = requests.get(url)
    base_url = urlparse(url).netloc   # get the base URL (domain)
    soup = str(BeautifulSoup(response.text, 'html.parser'))  # get the html page as a string

    urls = set()

    pattern = re.compile(r'href="(.*?)"')
    matches = pattern.findall(soup)

    for element in matches:
        element = urljoin(url, element)

        try:
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
        except:
            print(red + "there is a problem with the url: ", element)

    pattern = re.compile(regex)  # regex that finds all URLs in the plain text
    matches = pattern.findall(soup)

    for element in matches:
        element = urljoin(url, element)

        try:
            if not valid(element):
                continue                                    # same as the actions for the internal and external links
            if element in internal_url:
                continue
            if element in external_url:
                continue
            if base_url not in element:
                if element not in plainText_url:
                    print(cyan + "Plain Text Link")
                    check(element)
                    plainText_url.add(element)
        except:
            print(red + "there is a problem with the url: ", element)

    return urls


def crawler(url):                        # the crawler function crawls the websites using their internal links
    links = URL_link_extractor(url)
    for link in links:
        crawler(link)


def htmlPage_link_extractor(HTMLpage):              #scrape the html page to get the available links
    file = open(HTMLpage, encoding="utf8")
    soup = str(BeautifulSoup(file, 'html.parser'))
    file.close()

    urls = set()

    pattern = re.compile(r'href="(.*?)"')
    matches = pattern.findall(soup)

    for element in matches:
        if (re.match(regex, element) is not None):     #check if the link is type of url
            try:
                if not valild(element):               # check the validity of the link
                    continue
                if element in external_url:
                    continue
                print(cyan + "External Link")
                check(element)
                external_url.add(element)
            except:
                print(red + "there is a problem with the url: ", element)

    pattern = re.compile(regex)              # regex that finds all URLs in the plain text
    matches = pattern.findall(soup)

    for element in matches:
         try:
             if not valid(element):
                 continue                                    # same as the actions for the external links
             if element in plainText_url:
                 continue
             print(cyan + "Plain Text Link")
             check(element)
             plainText_url.add(element)
         except:
             print(red + "there is a problem with the url: ", element)
##########################################################################################################



def resultPrinter(urlORfile):                                # printing the result of the scraping and crawling
    print(gray + "=========================================================================================================")
    print(gray + "The result of scraping for the: " + urlORfile)
    print(gray + "\nTotal number of the valid links = ", len(internal_url) + len(external_url) + len(plainText_url))
    print(gray + "Total number of the valid internal_url links = ", len(internal_url))
    print(gray + "Total number of the valid external_url links = ", len(external_url))
    print(gray + "Total number of the valid links in the body text = ", len(plainText_url))
    print("=========================================================================================================")
    print(yellow + "Total number of the dead links (forbidden, not found, inaccessible) = ", len(broken_url))



if __name__ == "__main__":                             # main class to do the process


    Specifier = ''
    conditionsFileType = ('1', '2', '3', 'BASH')                # in order to be used for std:in

    CrawlingActivation = ''
    conditionsCrawling = ('Y', 'N')                              #in order to be used for the std:in

    FinishingCondition = ('End, end, END, E, e')

    while Specifier not in conditionsFileType:                   #specifying the input method
        Specifier = input(white + "Please specify the type of input method you want to use:\n\n1.a URL or multiple URLs\n2.an HTML page or multiple HTML pages\n3.a .txt file containing list of HTML pages\n\nPlease select one of the above options: [1/2/3] ")


    if Specifier == '1':                                                 #input method as url
        while CrawlingActivation.upper() not in conditionsCrawling:     #crawling activation or deactivation
            CrawlingActivation = input("\n" + white + "Do you want to keep the " + blue + "CRAWLING" + white + " Activated? [Y/n]  ")

        URLlist = []

        while True:
            print(yellow + "\nif you want to finish the url enterring process please write " + blue + "end" + yellow + " and press Enter")
            URL = input(blue + "\nPlease enter a url: ")                   #get the urls as input
            if (re.match(regex, URL) is not None):                #check the input if it's a url or not
                URLlist.append(URL)
            elif URL in FinishingCondition:                            #finish the input enterring using end + Enter
                break
            else:
                print(red + "The URL " + cyan + "< " + URL + " >" + red + " is not a correct url address (http[s]://url)")

        CrawlingActivation = CrawlingActivation.upper()
        if CrawlingActivation == ("Y"):                            #crawling activated
            for each in URLlist:
                crawler(each)
                resultPrinter(each)
                internal_url.clear()                                  #clear the data in order to perform correct results at the end
                external_url.clear()
                plainText_url.clear()
                broken_url.clear()
        if CrawlingActivation == ("N"):                              #crawling deactivated
            for each in URLlist:
                URL_link_extractor(each)
                resultPrinter(each)
                internal_url.clear()
                external_url.clear()
                plainText_url.clear()
                broken_url.clear()


    if Specifier == '2':                                       # input type for an html web page
        print(yellow + "Please make sure that you have copied the HTML file in the same directory as the script directory\n")
        print(yellow + "In this contirion the Crawler is desabled\n")
        htmlFile = input(blue + "Please enter the name of the html file to check: ")
        file = "./" + htmlFile
        try:
            htmlPage_link_extractor(file)
            resultPrinter(htmlFile)
        except:
            print(red + "you may not copy the index file into the script directory, or you entered the wrong name")


    if Specifier == '3':                                 # input type for a list of html pages
        print(yellow + "Please make sure that you have copied the HTML files in the same directory as the script directory\n")
        print(yellow + "Please make sure that you put the " + blue + "file contains the list of HTML files" + yellow + " in the same directory as the script directory\n")
        print(yellow + "In this condition the Crawler is disabled\n")
        textF = input(blue + "please enter the name of the file of the list (.txt file): ")
        textFile = "./" + textF
        try:
                textfile = open(textFile, "r")
                line = list(textfile)
                for files in line:
                    htmlfile = files.rstrip()
                    file = "./" + htmlfile
                    try:
                        htmlPage_link_extractor(file)
                        resultPrinter(htmlfile)
                        internal_url.clear()
                        external_url.clear()                                          # clear the variables to return the correct result at the end
                        plainText_url.clear()
                        broken_url.clear()
                    except:
                        print(red + "the file " + yellow + htmlFile + red + "is corrupted or does not exist in the same directory as the script directory"  )

        except:
            print(red + "list file does not exist or corrupted")



    if Specifier == 'BASH':                               # will be called from the bash directly
        print(yellow + "\nThis python script called from the Bash script to scrape the localhost webpage")
        URL = input("\nPlease enter your localhost server with the correct port: ")
        try:
            URL_link_extractor(URL)
            print(yellow + "\nThis python script called from the Bash script to scrape the localhost webpage")
            resultPrinter(URL)
        except:
            print(red + "\nyou may not use a vaild localhost IP or PORT on the github repository")
