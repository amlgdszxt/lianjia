# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 00:09:24 2020

@author: sse
"""

import numpy as np
import pandas as pd
df1 = pd.read_excel(r'D:\WORK\lianjia\学区高德坐标0806.xlsx')
df2 = pd.read_excel(r'D:\WORK\lianjia\小区高德坐标0806.xlsx')
df1 = df1[df1['纬度'] > 0].reset_index()
df2 = df2[df2['纬度'] > 0].reset_index()


n1 = df1.shape[0]
n2 = df2.shape[0]
df1['key'] = 1
df2['key'] = 1
df = df1.merge(df2,on = 'key')
df['distance'] = np.sqrt( (df['纬度_x'] - df['纬度_y'])**2 + (df['经度_x'] - df['经度_y'])**2 )
df.sort_values('distance',inplace = True)
#df.iloc[0]

res = pd.DataFrame(columns = df.columns)
while df.iloc[0]['distance'] <= 0.0015:
    row = df.iloc[0]
    res = res.append(row,ignore_index = True)
    df = df[df['index_x'] != row['index_x']]
    df = df[df['index_y'] != row['index_y']]
    print(res.shape[0])

res['index'] = res['index_x'].astype(int)
res1 = df1.merge(res,'left',on = 'index')
res1.to_clipboard()

