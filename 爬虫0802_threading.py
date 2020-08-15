# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 16:58:12 2020

@author: sse
"""
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 10:25:18 2020

@author: sse
"""

import urllib
import http.cookiejar as hc
import re
import random
import threading
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time

#创建一个cookiejar对象，用来存储获取的cookie
cookie = hc.CookieJar()
#DataFrame
df = pd.DataFrame(columns = ['名称','链接','建筑年代', '建筑类型', '物业费用', '物业公司', '开发商', '楼栋总数', '房屋总数', '附近门店', '坐标'])


def souper(url):
    try:
        req = urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'})
        source_code = urllib.request.urlopen(req,timeout=5).read()
        plain_text=source_code.decode()#,errors='ignore')   
        soup = BeautifulSoup(plain_text)
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print(e)
    except Exception as e:
        print(e)
    return soup

def page_opener(region,i,cookie):
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
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print(e)
    except Exception as e:
        print(e)
    return soup


def xq_opener(url,refer,cookie):
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding':'utf-8',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Host':'sh.lianjia.com',
        'Referer':refer,
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    }
    try:
        req = urllib.request.Request(url=url,headers=headers)
        source_code = opener.open(req,timeout=10).read()
        plain_text=source_code.decode()#,errors='ignore')   
        soup = BeautifulSoup(plain_text)
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print(e)
    except Exception as e:
        print(e)
    return soup
    
region="changning"
i=0
url="http://sh.lianjia.com/xiaoqu/rs"+region+"/"
soup = souper(url)


d = int(soup.find('div',{'class':'resultDes clear'}).text.split(' ')[1])
total_pages = int(np.ceil(d / 30))

pagethreads=[]
threads=[]
res = []

def page_test(region,i,cookie):
    soup = page_opener(region,i,cookie)
    xiaoqu_list=soup.findAll('div',{'class':'info'})
    nxq = len(xiaoqu_list)
    for j in range(nxq):
        t=threading.Thread(target=test,args=(i,j,xiaoqu_list,region,cookie))
        threads.append(t)
        print(i,j)
    
def test(i,j,xiaoqu_list,region,cookie):
    xq = xiaoqu_list[j]
    info_dict={}
    xqname = xq.a.text
    xqurl = xq.a.attrs['href']
    info_dict.update({'名称':xqname})
    info_dict.update({'链接':xqurl})
    soup = xq_opener(xqurl,"http://sh.lianjia.com/xiaoqu/pg%drs%s/" % (i+1,region),cookie)
    keys = soup.findAll('span',{'class':'xiaoquInfoLabel'})
    values = soup.findAll('span',{'class':'xiaoquInfoContent'})
    dz = soup.find('div',{'class':'detailDesc'}).text
    avgprice = '暂无'
    try:
        avgprice = soup.find('span',{'class':'xiaoquUnitPrice'}).text
    except:
        pass
    pattern = re.compile('resblockPosition:\'(.*?)\',')
    location = pattern.findall(soup.text)[0]
    info_dict.update({'地址':dz,'挂牌均价':avgprice})
    info_dict.update(dict(zip([key.text for key in keys],[value.text for value in values])))
    info_dict.update({'坐标':location})
    res.append(pd.Series(info_dict))
    print(str(i)+','+str(j)+'\n')


for i in range(total_pages):
    tt=threading.Thread(target=page_test,args=(region,i,cookie))
    pagethreads.append(tt)
    print(i)

for tt in pagethreads:
    tt.start()
for tt in pagethreads:
    tt.join()

print(len(threads))

for t in threads:
    t.start()
for t in threads:
    t.join()
    
print(len(res))

df = pd.DataFrame(res)
df.to_clipboard()
