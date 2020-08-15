# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 00:44:11 2020

@author: sse
"""


'''
import numpy as np
import pandas as pd
from urllib.request import urlopen, quote
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
    url = 'http://api.map.baidu.com/geocoding/v3/'
    output = 'json'
    ak = keys['baidu'] # 百度地图ak，具体申请自行百度，提醒需要在“控制台”-“设置”-“启动服务”-“正逆地理编码”，启动
    city = '上海市'
    address = quote(address) # 由于本文地址变量为中文，为防止乱码，先用quote进行编码
    city = quote(city)
    uri = 'http://api.map.baidu.com/geocoding/v3/?address=' + address + '&output=xml&city=' + city + '&ak=' + ak + '&callback=showLocation'
    req = urlopen(uri)
    res = req.read().decode() 
    soup = BeautifulSoup(res)
    lat = float(soup.findAll('lat')[0].text)
    lng = float(soup.findAll('lng')[0].text)
    return lat,lng   # 纬度 latitude   ，   经度 longitude  ，

df = pd.read_excel(r'D:\WORK\lianjia\长宁区小学对应学区地址.xlsx')
df['纬度'] = 0.0
df['经度'] = 0.0

for idx,row in df.iterrows():
    t1 = time.perf_counter()
    try:
        add = df.loc[idx,'地址']
        lat,lng = getlnglat(add)
        df.loc[idx,'纬度'] = lat
        df.loc[idx,'经度'] = lng
        print(idx,add,lat,lng)
    except Exception as e:
        print(idx,add,e)
    t2 = time.perf_counter()
    print('耗时:',t2-t1)

df.to_clipboard()
'''
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 00:44:11 2020

@author: sse
"""
import numpy as np
import pandas as pd
import urllib
import requests
from bs4 import BeautifulSoup
import time

def getlnglat(address):
    #address = '华山路1038弄（163号165号167号169号171号）'
    url = 'https://restapi.amap.com/v3/geocode/geo'
    city = '上海'
    city = urllib.parse.quote(city)
    ak = keys['amap']
    address = urllib.parse.quote(address)
    uri = url + '?' + 'key=' + ak + '&address=' + address + '&city=' + city
    req = requests.get(uri)
    temp = req.json()
    status = temp['status']
    if status == '1':
        location = temp['geocodes'][0]['location']
        lng,lat = location.split(',')
    return float(lng),float(lat)

df = pd.read_excel(r'D:\WORK\lianjia\学区高德坐标0806.xlsx')
df['纬度'] = 0.0
df['经度'] = 0.0

for idx,row in df.iterrows():
    t1 = time.perf_counter()
    try:
        add = df.loc[idx,'地址']
        lng,lat = getlnglat(add)
        df.loc[idx,'纬度'] = lat
        df.loc[idx,'经度'] = lng
        print(idx,add,lat,lng)
    except Exception as e:
        print(idx,add,e)
    t2 = time.perf_counter()
    print('耗时:',t2-t1)

df.to_clipboard()
