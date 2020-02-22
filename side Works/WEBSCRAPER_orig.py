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

internal = set()
external = set()
Plain_TEXT_Link = set()
ALLURLS = set()

count = 0

def check(url):         # check the url in order to find the broken links
    global count

    try:
        resp = urllib.request.urlopen(url, timeout=10)
        if resp.code == 200:
            print(green + " working well " + url)
    except HTTPError as e:
        print(red + 'The server couldn\'t fulfill the request for the: ' + url)
        print(red + 'Error code: ', e.code)
        count += 1

    except URLError as e:
        print(red + 'We failed to reach a server for the: ' + url)
        print(red + 'Reason: ', e.reason)
        count += 1

def is_valild(url):        # check the validity of the url using the url protocol and the domain
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def crawler(url):          # crawl the webSite (url) to extract all the available links
    response = requests.get(url)
    soup = str(BeautifulSoup(response.text, 'html.parser'))
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))

    urls = set()

    pattern = re.compile(r'href="(.*?)"')
    matches = pattern.findall(soup)

    for element in matches:                     # finding external links
        if element[0:4] == "http":
            ALLURLS.add(element)
            if is_valild(element):
                external.add(element)
                print(cyan + "External Link")
                check(element)


        else:                                    # finding internal links
            element = urljoin(base_url, element)
            ALLURLS.add(element)
            if is_valild(element):
                internal.add(element)
                print(cyan + "Internal Link")
                check(element)



    for element in soup.split():                       # finding the links inside the body text outside of the special tags
        if (element[0:4] == "http") and ("://" in element) and ("href") not in element:
            path = urlparse(element).path
            path = path.replace("~", ".")
            path = path.replace("!", ".")
            path = path.replace("@", ".")
            path = path.replace("#", ".")
            path = path.replace("$", ".")
            path = path.replace("%", ".")
            path = path.replace("^", ".")
            path = path.replace("&", ".")
            path = path.replace("*", ".")
            path = path.replace("+", ".")
            path = path.replace("=", ".")
            path = path.replace("{", ".")
            path = path.replace("}", ".")
            path = path.replace("[", ".")
            path = path.replace("]", ".")
            path = path.replace(":", ".")
            path = path.replace(";", ".")
            path = path.replace("'", ".")
            path = path.replace('"', '.')
            path = path.replace("|", ".")
            path = path.replace("<", ".")
            path = path.replace(">", ".")
            path = path.replace(",", ".")

            if "." in path:
                pattern = re.compile(r'(.*?)\.')
                match = pattern.findall(path)
                for each in match:
                    if each != "":
                        newPath = urlparse(element).scheme + "://" + urlparse(element).netloc + each
                        ALLURLS.add(newPath)
                        if is_valild(newPath):
                            Plain_TEXT_Link.add(newPath)
                            print(cyan + "Link in the body text")
                            check(newPath)

            else:
                newPath = urlparse(element).scheme + "://" + urlparse(element).netloc + path
                ALLURLS.add(newPath)
                if is_valild(newPath):
                    Plain_TEXT_Link.add(newPath)
                    print(cyan + "Link in the body Text")
                    check(newPath)


if __name__ == "__main__":                             # main class to do the process


    URL = input("please enter a url like http(s);//url  ")
    crawler(URL)

    print(magneta + "Total number of the available links in the " + URL + " is " + str(len(ALLURLS)))
    print("=========================================================================================================")
    print(gray + "Total number of the valid links = ", len(internal) + len(external) + len(Plain_TEXT_Link))
    print(gray + "Total number of the valid internal links = ", len(internal))
    print(gray + "Total number of the valid external links = ", len(external))
    print(gray + "Total number of the valid links in the body text = ", len(Plain_TEXT_Link))
    print("=========================================================================================================")
    print(yellow + "Total number of the dead links (forbidden, not found, inaccessible) are ", count)