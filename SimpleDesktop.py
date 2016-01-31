from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re

pages = set()
images = set()

def getPages(pageUrl):
    global pages
    try:
        html = urlopen("http://simpledesktops.com" + pageUrl)
        print(pageUrl)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html, "html.parser")
    except:
        return None
    
    getImgLinks(bsObj)

    try:
        nextPage = bsObj.find("a",{"class":"more"})
    except:
        return None
    if 'href' in nextPage.attrs:
        if nextPage.attrs['href'] not in pages:
            newPage = nextPage.attrs['href']
            pages.add(newPage)
            #getPages(newPage)


def getImgLinks(obj):
    global images
    if obj == None:
        print("Error")
    else:
        imgLink = obj.findAll("a",href=re.compile("^(/browse/desktops/)+?"))
        for link in imgLink:
            if 'href' in link.attrs:
                if link.attrs['href'] not in images:
                    newImgLink = link.attrs['href']
                    print(newImgLink)
                    images.add(newImgLink)
                    getImg(newImgLink)


def getImg(imgLink):
    try:
        html = urlopen("http://simpledesktops.com" + imgLink)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html, "html.parser")
        imgUrl = bsObj.find("div",{"class":"desktop"}).img
    except:
        return None
    if imgUrl == None:
        print("Error img")
    else:
        if 'src' in imgUrl.attrs:
            url = imgUrl.attrs['src']
            url = re.match("^.+?(\.png)", url)
            print(url.group(0))


getPages("/browse/")
