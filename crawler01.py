# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup

import csv
import time
import sys

YOMIKATA1 = "【読み方】："
YOMIKATA2 = "【読み方】；"
YOMIKATA3 = "【読み方】"


def scraper(url):

    try:
        html = urlopen(url)
    except URLError as e:
        print(e)
        return None

    soup = BeautifulSoup(html.read(), "lxml")
    linkDivs = soup.findAll("div", {"class": "archives"})
    print("linkDivs = %s\n" % linkDivs)

    linkHeaders = []
    for i, linkDiv in enumerate(linkDivs):
        print("linkDiv[%d] = %s" % (i, linkDiv))

        linkHeaders.append(linkDiv.findAll("h3"))

    print("linkHeaders = %s\n" % linkHeaders)

    addresses = []
    for linkHeader in linkHeaders:

        print("linkHeader = %s" % linkHeader)
        print("linkHeader type = %s" % type(linkHeader))

        for link in linkHeader:
            linkURL = link.find("a")
            print(linkURL)

        # linkAddresses = linkHeader.find("a")
        # print("linkAddresses = %s\n" % linkAddresses)

        # if 'href' in linkAddresses.attrs:
        #     addresses.append(linkAddresses.attrs['href'])

    print("addresses = %s\n" % addresses)

    # for link in linkAddresses:
    #     print("header text= %s" % link.get_text())

    # print(linkHeaders)

    # headers = [header.get_text() for header in linkHeaders]
    # print(headers)

    # addresses = []
    # for link in linkHeaders:

    #     linkAdress = link.find("a")
    #     # print(linkAdress)

    #     if 'href' in linkAdress.attrs:
    #         addresses.append(linkAdress.attrs['href'])

    yomi = []
    for address in addresses:
        yomi.append(getYomi(address))

    print("%s\n" % yomi)

    saveData(headers, yomi)
    time.sleep(3)
    return True


def getNextLink(url):

    html = urlopen(url)
    soup = BeautifulSoup(html.read(), "lxml")

    nextLink = soup.find("div", {"class": "pagination"}).find(
        "a", text="次のページ ›")

    # if ('href' in nextLink.attrs) or (nextLink is not None):
    #     nextLinkUrl = nextLink.attrs['href']
    #     return nextLinkUrl
    # else:
    #     return None
    if nextLink is not None:
        if 'href' in nextLink.attrs:
            nextLinkUrl = nextLink.attrs['href']
            return nextLinkUrl
        else:
            return None
    else:
        return None


def getYomi(url):

    html = urlopen(url)
    soup = BeautifulSoup(html.read(), "lxml")

    yomi = soup.findAll("p")[1]

    cleanTexts = "\n".join(yomi.strings)
    cleanTexts = cleanTexts.split('\n')

    while cleanTexts.count("") > 0:
        cleanTexts.remove("")

    print("cleanText= %s" % cleanTexts)
    cleanText = cleanTexts[0]
    cleanText = cleanText.replace(YOMIKATA1, "")
    cleanText = cleanText.replace(YOMIKATA2, "")
    cleanText = cleanText.replace(YOMIKATA3, "")

    return cleanText


def saveData(headers, yomis):

    f = open('data.csv', 'a', newline='', encoding='utf-8')

    try:
        writer = csv.writer(f)

        for header, yomi in zip(headers, yomis):
            writer.writerow((header, yomi))
    finally:
        f.close()


def main():

    argvs = sys.argv
    argc = len(argvs)

    if argc == 2:
        targetUrl = argvs[1]

        i = 1
        page = "/page"
        newTargetUrl = targetUrl

        while True:
            print(newTargetUrl)
            isURLError = scraper(newTargetUrl)
            # targetUrl = getNextLink(targetUrl)

            i = i + 1
            newPage = page + str(i)
            newTargetUrl = targetUrl + newPage

            # if targetUrl is None:
            #     break
            if isURLError is None:
                break

        print("Finish")

    else:
        print("Can't find target URL. Please input target URL.")


if __name__ == '__main__':
    main()
