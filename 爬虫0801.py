# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 23:54:54 2020

@author: sse
"""
import urllib
import re
import random
import threading
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time

df = pd.DataFrame(columns = ['名称','链接','建筑年代', '建筑类型', '物业费用', '物业公司', '开发商', '楼栋总数', '房屋总数', '附近门店', '坐标'])

#Some User Agents
hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
    {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
    {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
    {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
    {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]


def souper(url):
    try:
        req = urllib.request.Request(url,headers=hds[random.randint(0,len(hds)-1)])
        source_code = urllib.request.urlopen(req,timeout=5).read()
        plain_text=source_code.decode()#,errors='ignore')   
        soup = BeautifulSoup(plain_text)
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print(e)
    except Exception as e:
        print(e)
    return soup


region="changning"
url="http://sh.lianjia.com/xiaoqu/rs"+region+"/"
soup = souper(url)


d="d="+soup.find('div',{'class':'page-box house-lst-page-box'}).get('page-data')
exec(d)
total_pages=d['totalPage']

for i in range(total_pages):
    start_time = time.clock()
    url_page=u"http://sh.lianjia.com/xiaoqu/pg%drs%s/" % (i+1,region)
#----------------------------------------------------------------------------
    soup = souper(url_page)
    xiaoqu_list=soup.findAll('div',{'class':'info'})
    nxq = len(xiaoqu_list)
    #xq = xiaoqu_list[0]
    for j in range(nxq):
        xq = xiaoqu_list[j]
        info_dict={}
        xqname = xq.a.text
        xqurl = xq.a.attrs['href']
        info_dict.update({'名称':xqname})
        info_dict.update({'链接':xqurl})
        soup = souper(xqurl)
        keys = soup.findAll('span',{'class':'xiaoquInfoLabel'})
        values = soup.findAll('span',{'class':'xiaoquInfoContent'})
        pattern = re.compile('resblockPosition:\'(.*?)\',')
        location = pattern.findall(soup.text)[0]
        info_dict = dict(zip([key.text for key in keys],[value.text for value in values]))
        info_dict.update({'坐标':location})
        df = df.append(pd.Series(info_dict),True)
        print(i,'/',total_pages,': ',j,'/',nxq,xqname)
    end_time = time.clock()
    print('耗时:',end_time-start_time)

