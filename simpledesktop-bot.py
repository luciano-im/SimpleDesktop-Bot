import os
import re
import shutil
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup


def requestPage(url):
    """
    Request pages and parse HTML response
    """
    try:
        raw_html = requests.get(url)
        try:
            html = BeautifulSoup(raw_html.text, features='html.parser')
            return html
        except:
            print('Error parsing HTML code')
            return None
    except HTTPError as e:
        print(e.reason)
        return None


def getPageContent(url):
    """
    Get wallpaper and next page data from requested page
    """
    images = []
    next_page = None
    
    html = requestPage(url)
    if html is not None:
        # Search wallpapers URL
        wallpapers = html.find_all('div', {'class': 'desktop'})
        for wp in wallpapers:
            img = wp.find('img')
            images.append(img.attrs['src'])
    
        # Search for next page URL
        try:
            more_button = html.find('a', {'class':'more'})
            next_page = more_button.attrs['href']
        except:
            pass
    
    return {'images': images, 'next_page': next_page}


def downloadWallpaper(wallpapers, directory):
    """
    Process wallpaper downloads
    """
    for url in wallpapers:
        match_url = re.match('^.+?(\.png|jpg)', url)
        if match_url:
            formated_url = match_url.group(0)
            filename = formated_url[formated_url.rfind('/')+1:]
            file_path = os.path.join(directory, filename)
            print(file_path)

            if not os.path.exists(file_path):
                with requests.get(formated_url, stream=True) as wp_file:
                    with open(file_path, 'wb') as output_file:
                        shutil.copyfileobj(wp_file.raw, output_file)
        else:
            print('Wallpaper URL is invalid')


def processPage(url, path, download_directory):
    """
    Recursive function that deliver pages to request and wallpaper's data to the other functions
    """
    print('\nPATH:', path)
    print('=========================')

    wallpapers = getPageContent(url + path)
    if wallpapers['images']:
        downloadWallpaper(wallpapers['images'], download_directory)
    else:
        print('This page does not contain any wallpaper')
    if wallpapers['next_page']:
        processPage(url, wallpapers['next_page'], download_directory)
    else:
        print('THIS IS THE END, BUDDY')


if __name__ == '__main__':
    # Run, run, run
    url = 'http://simpledesktops.com'
    first_path = '/browse/'
    download_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wallpapers')
    
    # Create download directory if it does not exists
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)
    
    # Start crawling
    processPage(url, first_path, download_directory)