
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 22:41:22 2021

@author: sse
"""

import httpx
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://sh.esf.fang.com'

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
    
#学校   
school_res = pd.DataFrame()   
current_url = url
next_url = '/school'


while True:
    headers['refer'] = current_url
    current_url = url + next_url
    r = httpx.get(current_url, headers = headers)
    r.encoding = 'gbk'
    soup = BeautifulSoup(r.text,'html.parser')
    a = soup.findAll('dl',{'class':'list clearfix'})

    df = pd.DataFrame({
        'school_name':[a0.findAll('p',{'class':'title'})[0].text for a0 in a],
        'community_number':[a0.findAll('p',{'class':'mt13 bold'})[0].text.replace('\n','') for a0 in a],
        'school_address':[a0.findAll('p',{'class':'gray6 mt13'})[0].text for a0 in a],
        'school_tags':[[b0.text for b0 in a0.findAll('p',{'class':'mt15'})[0].findAll('span')] for a0 in a],
        'price_range':[[b0.text for b0 in a0.findAll('p',{'class':'danjia2 red'})[0].findAll('strong')] for a0 in a],
        'forsale_number':[a0.findAll('a',{'class':'hsNum blue alignR'})[0].find('strong').text for a0 in a],
        'url':[a0.findAll('p',{'class':'title'})[0].a.attrs['href'] for a0 in a]
    })

    school_res = school_res.append(df,ignore_index = True)
    
    if soup.find('a',{'id':'PageControl1_hlk_next'}):
        next_url = soup.find('a',{'id':'PageControl1_hlk_next'}).attrs['href']
    else:
        break
    print(current_url)
    
school_res.to_clipboard()
    
    
#小区
community_res = pd.DataFrame()
headers['refer'] = url + '/school/'
for i,row in school_res.iterrows():
    lnk = row['url']
    n = int(row['community_number'][:-3])
    for page in range(1,2 + n//20):
        current_url = 'https://sh.esf.fang.com/school/%s/xiaoqu/%d' % (lnk[8:-4],page)
        r = httpx.get(current_url, headers = headers)
        r.encoding = 'gbk'
        dct = eval(r.text)
        if dct['Message'] == 'OK':
            df = pd.DataFrame(dct['ProjInfo'])
            df['school_name'] = row['school_name'] 
            community_res = community_res.append(df,ignore_index = True)
        else:
            raise Exception(i,page)
        print(i,row['school_name'],page)
#    r = httpx.get(current_url, headers = headers)
#    r.encoding = 'gbk'
#    soup = BeautifulSoup(r.text,'html.parser')
#    a = soup.findAll('div',{'class':'houseInfo'})
    
#    df = pd.DataFrame({
#        'school_name':row['school_name'],
#        'community_name':[a0.findAll('a',{'class':'title'})[0].text for a0 in a],
#        'forsale_number':[a0.findAll('a',{'class':'red ml30'})[0].find('strong').text if a0.findAll('a',{'class':'red ml30'}) else np.NaN for a0 in a],
#        'avg_price':[[child for child in a0.p.children][2].text for a0 in a],
#        'community_age':[[child for child in a0.p.children][5] for a0 in a],
#        'distance_from_school':[[child for child in a0.p.children][7].replace('\r\n        ','') for a0 in a],
#        'fitted blocks':[a0.select('p')[-1].text.replace('\n','') for a0 in a]
#    })

#    community_res = community_res.append(df,ignore_index = True)
    
community_res.to_clipboard()
