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
df1['xiaoqu'] = ''
df1['buldings'] = ''
df1['hushu'] = ''
df1['baidujingdu'] = 0.0
df1['baiduweidu'] = 0.0
df1['lianjiazuobiao'] = ''
df1.sort_values('户数',ascending = False,inplace = True)
df1.reset_index(drop = True,inplace = True)

for i in range(n1):
    min_distance = 10000.0
    best_j = -1
    for j in range(n2):
        distance = np.sqrt( (df1.iloc[i]['纬度'] - df2.iloc[j]['纬度'])**2 + (df1.iloc[i]['经度'] - df2.iloc[j]['经度'])**2 )
        if distance < min_distance:
            min_distance = distance
            best_j = j
    df1.loc[i,'distance'] = min_distance
    df1.loc[i,'xiaoqu'] = df2.loc[best_j,'名称']
    df1.loc[i,'hushu'] = df2.loc[best_j,'房屋总数']
    df1.loc[i,'buldings'] = df2.loc[best_j,'楼栋总数']
    df1.loc[i,'lianjiazuobiao'] = df2.loc[best_j,'链家坐标']
    df1.loc[i,'baidujingdu'] = df2.loc[best_j,'经度']
    df1.loc[i,'baiduweidu'] = df2.loc[best_j,'纬度']
    print(i,'/',n1)
    
df1.to_clipboard()
