# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 22:23:22 2020

@author: sse
"""
import numpy as np
import pandas as pd
df1 = pd.read_excel(r'D:\WORK\lianjia\小区高德坐标0806.xlsx')
df2 = pd.read_excel(r'D:\WORK\lianjia\学区高德坐标0806.xlsx')
n1 = df1.shape[0]
n2 = df2.shape[0]

df1['户数'] = df1.loc[:,'房屋总数'].str[:-1].astype(int)
df1['distance'] = 10000.0
df1['校名'] = ''
df1['招生地块'] = ''
df1['地址'] = ''
df1['学区纬度'] = 0.0
df1['学区经度'] = 0.0
df1['j'] = 0

df1.sort_values('户数',ascending = False,inplace = True)
df1.reset_index(drop = True,inplace = True)
n1 = 10
for i in range(n1):
    min_distance = 10000.0
    best_j = -1
    for j in range(n2):
        distance = np.sqrt( (df1.iloc[i]['纬度'] - df2.iloc[j]['纬度'])**2 + (df1.iloc[i]['经度'] - df2.iloc[j]['经度'])**2 )
        if distance < min_distance and distance <= 0.002:
            min_distance = distance
            best_j = j
    if min_distance <= 0.002:
        df1.loc[i,'distance'] = min_distance
        df1.loc[i,'校名'] = df2.iloc[best_j]['校名']
        df1.loc[i,'招生地块'] = df2.iloc[best_j]['招生地块']
        df1.loc[i,'地址'] = df2.iloc[best_j]['地址']
        df1.loc[i,'学区纬度'] = df2.iloc[best_j]['纬度']
        df1.loc[i,'学区经度'] = df2.iloc[best_j]['经度']
        df1.loc[i,'j'] = best_j
        
        df2.drop(index = df2.index[best_j],inplace = True)
        n2 = df2.shape[0]
    print(i,'/',n1)
    
df1.to_clipboard()
