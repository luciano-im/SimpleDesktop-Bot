import os
import re
from urllib.request import urlopen, urlretrieve
from urllib.error import HTTPError
from bs4 import BeautifulSoup

pages = set()
images = set()
downloadDirectory = "wallpapers"
numImg = 0

def getPages(pageUrl):
    global pages
    try:
        html = urlopen("http://simpledesktops.com" + pageUrl)
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
            getPages(newPage)


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
    global numImg
    path = re.match("^(http://static.simpledesktops.com/uploads/desktops/)+([0-9]+/)+", imgLink)
    path = imgLink.replace(path.group(0), "")
    #To avoid freeze with img named ".png"
    if path == ".png":
        numImg += 1
        path = "localImg"+str(numImg)+path
    directory = os.path.dirname(os.path.abspath(__file__))+"/"+downloadDirectory
    
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    return directory+"/"+path


getPages("/browse/32")
