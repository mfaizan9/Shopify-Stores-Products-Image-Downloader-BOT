import requests
from bs4 import BeautifulSoup
import os
from concurrent.futures import ThreadPoolExecutor
import re
import urllib.request
import time




product_links = []

print('*-*-*-*-*-*-*-*-*-*-*-*-*-*- \n')
print('Type "done" after entering links\n')
print('*-*-*-*-*-*-*-*-*-*-*-*-*-*- \n')

while True:
    link = input('Enter Product Link:  ')
    print('\n')
    product_links.append(link)
    if link == 'done' or link == 'Done':
        break

# DOWNLOAD FUNCTION
def image_dl(url , path , filename):
    full_path = path + filename + '.jpg'
    urllib.request.urlretrieve(url , full_path)


# DOWNLOAD IN DIRECTORY
def download(url):
    image_list = []
    url_split = url.split('products/')
    image_nishani = url_split[-1].replace('/', '') # folder name
    image_kws = image_nishani.split('-')
    # print(image_kws)
    del image_kws[-1]
    # print(image_kws)
    product_name = image_nishani.replace('-', ' ').title()
    try:
        plist = product_name.split('?')
        product_name = plist[0]
    except:
        pass
    # print(product_name)
    r = requests.get(url).text
    soup = BeautifulSoup(r , 'html.parser')
    img_tags = soup.find_all('img')
    try:
        product_title = soup.find('h1').text.strip()
        # print(product_title)
    except:
        product_title = product_name
    for img_tag in img_tags:
        try:
            image_link = img_tag.get('src')

            if image_link is not None:
                # print(image_link)
                # print('Hello')
                # print(image_kws[2])
                if any(i in image_link for i in image_kws):
                    # print('Hello')
                    if image_link[0:2]=='//':
                        image_link = 'https:'+image_link
                        # print(image_link)
                    else:
                        pass
                    image_link = image_link.replace('_small', '')
                    image_link = image_link.replace('_medium', '')
                    image_link = image_link.replace('_large', '')
                    # print(image_link)
                    image_list.append(image_link)
                newlist = list(dict.fromkeys(image_list))
                # print(newlist)
        except:
            pass
    
    # NEW LIST
    # Make Folder
    os.mkdir(product_title)
    for j in newlist:
        # print(j)
        filename = product_title + ' ' + str(newlist.index(j))
        try:
            image_dl(j, product_title+'/' , filename)
        except:
            pass



print('Downloading Images.')
# Multi-threading
try:
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download, product_links)

    print('Download FINISHED')

    time.sleep(3)
except:
    print('Cannot Download')

