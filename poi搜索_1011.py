# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 18:46:04 2020

@author: sse
"""


import numpy as np
import pandas as pd
import urllib
import requests
from bs4 import BeautifulSoup
import time

from xml.dom.minidom import parse
import xml.dom.minidom
DOMTree = xml.dom.minidom.parse('D:/keys.xml')
collection = DOMTree.documentElement
keys = {}
keylist = collection.getElementsByTagName("key")
for key in keylist:
    keys.update({key.getAttribute("name"):key.getElementsByTagName('value')[0].childNodes[0].data})

def getlnglat(address):
    address = '学而思培优'
    #address = '华山路1038弄（163号165号167号169号171号）'
    offset = 20
    url = 'https://restapi.amap.com/v3/place/text'
    city = '上海'
    city = urllib.parse.quote(city)
    ak = keys['amap']
    address = urllib.parse.quote(address)
    uri = url + '?' + 'key=' + ak + '&keywords=' + address + '&city=' + city + '&children=1&offset=' + str(offset) + '&page=1&extensions=all'
    req = requests.get(uri)
    temp = req.json()
    count = temp['count']
    df = pd.DataFrame()
    for page in range(1,int(count)//offset+2):
        uri = url + '?' + 'key=' + ak + '&keywords=' + address + '&city=' + city + '&children=1&offset=' + str(offset) + '&page=' + str(page) + '&extensions=all'
        req = requests.get(uri)
        temp = req.json()
        pois = temp['pois']
        for i in range(len(pois)):
            poi = pois[i]
            df = df.append(pd.Series({item:poi[item] for item in ['name','address','adname','business_area','location']}),ignore_index=True)
    return(df)
    

//restapi.amap.com/v3/place/text?key=您的key&keywords=精锐教育&types=&city=上海&children=1&offset=1000&page=1&extensions=all