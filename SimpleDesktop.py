import os
import re
from urllib.request import urlopen, urlretrieve
from urllib.error import HTTPError
from bs4 import BeautifulSoup

pages = set()
images = set()
downloadDirectory = "wallpapers"

def getPages(pageUrl):
    global pages
    try:
        html = urlopen("http://simpledesktops.com" + pageUrl)
        #print(pageUrl)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html)
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
        print("Error: Invalid URL.")
    else:
        imgLink = obj.findAll("a",href=re.compile("^(/browse/desktops/)+?"))
        for link in imgLink:
            if 'href' in link.attrs:
                if link.attrs['href'] not in images:
                    newImgLink = link.attrs['href']
                    #print(newImgLink)
                    images.add(newImgLink)
                    getImg(newImgLink)


def getImg(imgLink):
    try:
        html = urlopen("http://simpledesktops.com" + imgLink)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html)
        imgUrl = bsObj.find("div",{"class":"desktop"}).img
    except:
        return None
    if imgUrl == None:
        print("Error: IMG doesn't exists.")
    else:
        if 'src' in imgUrl.attrs:
            url = imgUrl.attrs['src']
            url = re.match("^.+?(\.png)", url)
            print(url.group(0))
            urlretrieve(url.group(0), getDownloadPath(url.group(0), downloadDirectory))

def getDownloadPath(imgLink, downloadDirectory):
    path = imgLink.replace(re.compile("^(http://static.simpledesktops.com/uploads/desktops/)?([0-9]+/)+"), "")
    path = downloadDirectory+"/"+path
    directory = os.path.dirname(path)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    return path


getPages("/browse/")
