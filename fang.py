# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 09:36:12 2021

@author: sse
"""


from hyper.contrib import HTTP20Adapter
from hyper import HTTPConnection

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time


conn = HTTPConnection('sh.esf.fang.com:443')
conn.request('GET', 'school', None, None)
resp = conn.get_response()

s = resp.read(decode_content='utf-8')


url = 'https://sh.esf.fang.com/school/'
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
url_page=u"http://sh.lianjia.com/xiaoqu/pg%drs%s/" % (i+1,region)
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding':'utf-8',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'Host':'sh.lianjia.com',
    'Referer':'http://sh.lianjia.com/xiaoqu/pg%drs%s/' % (i,region),
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
}
if i == 0:
    headers.pop('Referer')
try:
    req = urllib.request.Request(url=url_page,headers=headers)
    source_code = opener.open(req,timeout=5).read()
    plain_text=source_code.decode()#,errors='ignore')   
    soup = BeautifulSoup(plain_text)
    
        
headers = {'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'accept-encoding':'gzip, deflate, br',
'accept-language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
'sec-fetch-dest':'document',
'sec-fetch-mode':'navigate',
'sec-fetch-site':'none',
'sec-fetch-user':'?1',
'upgrade-insecure-requests':'1',
'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.75'
}
sessions = requests.session()
sessions.mount(url, HTTP20Adapter())
response = sessions.get(url = url,headers = headers)


# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 22:41:22 2021

@author: sse
"""

import httpx
from bs4 import BeautifulSoup

headers = {

        'accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding':
        'gzip, deflate, br',
        'accept-language':
        'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'sec-fetch-dest':
        'document',
        'sec-fetch-mode':
        'navigate',
        'sec-fetch-site':
        'none',
        'sec-fetch-user':
        '?1',
        'upgrade-insecure-requests':
        '1',
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.75'
                }
r = httpx.get('https://sh.esf.fang.com/school/', headers = headers)
r.encoding = 'gbk'
soup = BeautifulSoup(r.text,'html.parser')
a = soup.findAll('dl',{'class':'list clearfix'})
