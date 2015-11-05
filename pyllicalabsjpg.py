from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
import re
import os

def jpg(identifier, title="titre", firstpage=1, lastpage=1):
    lastpage+=1
    listpage = range(firstpage, lastpage)
    for page in listpage:
        jpgfile = title + "_" + str(page) + ".jpg"
        url = 'http://gallica.bnf.fr/iiif/ark:' + identifier + '/f' + str(page) + '/full/3000/0/native.jpg'
        urllib.request.urlretrieve(url, jpgfile)
   
    
             
