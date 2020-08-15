# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 00:03:56 2020

@author: sse
"""


import numpy as np
import pandas as pd
import urllib
import requests
from bs4 import BeautifulSoup
import time
import math
from xml.dom.minidom import parse
import xml.dom.minidom
DOMTree = xml.dom.minidom.parse('D:/keys.xml')
collection = DOMTree.documentElement
keys = {}
keylist = collection.getElementsByTagName("key")
for key in keylist:
    keys.update({key.getAttribute("name"):key.getElementsByTagName('value')[0].childNodes[0].data})


def GCJ2WGS(location):
    # location格式如下：locations[1] = "113.923745,22.530824"
    lon = float(location[0:location.find(",")])
    lat = float(location[location.find(",") + 1:len(location)])
    a = 6378245.0 # 克拉索夫斯基椭球参数长半轴a
    ee = 0.00669342162296594323 #克拉索夫斯基椭球参数第一偏心率平方
    PI = 3.14159265358979324 # 圆周率
    # 以下为转换公式
    x = lon - 105.0
    y = lat - 35.0
    # 经度
    dLon = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x));
    dLon += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0;
    dLon += (20.0 * math.sin(x * PI) + 40.0 * math.sin(x / 3.0 * PI)) * 2.0 / 3.0;
    dLon += (150.0 * math.sin(x / 12.0 * PI) + 300.0 * math.sin(x / 30.0 * PI)) * 2.0 / 3.0;
    #纬度
    dLat = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x));
    dLat += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0;
    dLat += (20.0 * math.sin(y * PI) + 40.0 * math.sin(y / 3.0 * PI)) * 2.0 / 3.0;
    dLat += (160.0 * math.sin(y / 12.0 * PI) + 320 * math.sin(y * PI / 30.0)) * 2.0 / 3.0;
    radLat = lat / 180.0 * PI
    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * PI);
    dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * PI);
    wgsLon = lon - dLon
    wgsLat = lat - dLat
    return ','.join([str(wgsLon),str(wgsLat)])

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
    return lng,lat

def getroute(add1,add2):
    ak = keys['amap']
    uri = 'https://restapi.amap.com/v3/direction/walking?origin=' + ','.join(add1) + '&destination=' + ','.join(add2) + '&key=' + ak
    req = requests.get(uri)
    temp = req.json()
    status = temp['status']
    if status == '1':
        polyline = temp['route']['paths'][0]['steps']
        return polyline
                
polyres = []
roadlist = ['镇宁路','延安西路','江苏路','愚园路']
roadlist.append(roadlist[0])
addlist = []
for i in range(len(roadlist)-1):
    addlist.append(getlnglat(roadlist[i] + roadlist[i+1] + '交叉口'))
addlist.append(addlist[0])
for i in range(len(addlist)-1):
    polyline= getroute(addlist[i], addlist[i+1])
    for poly in polyline:
        if float(poly['distance']) >= 10.0:
            print(addlist[i],addlist[i+1],poly['instruction'])
            polyres += poly['polyline'].split(';')
    
polyres = [GCJ2WGS(x) for x in polyres]
df = pd.DataFrame(polyres)
df.to_clipboard()
