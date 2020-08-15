# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 22:23:22 2020

@author: sse
"""
import numpy as np
import pandas as pd
df1 = pd.read_excel(r'D:\WORK\lianjia\学区高德坐标0809.xlsx')
df2 = pd.read_excel(r'D:\WORK\lianjia\小区高德坐标0809.xlsx')
df2.columns = ['名称', '链接', '原始地址', '截取地址', '挂牌均价', '建筑年代', '建筑类型', '物业费用', '物业公司', '开发商',
       '楼栋总数', '房屋总数', '附近门店', '坐标', '高德纬度', '高德经度']

res = pd.DataFrame()


temp = df1.merge(df2,'inner',left_on = '地址',right_on = '名称')
temp['匹配方式'] = '学区地址-小区名称'
temp['distance'] = 0.0
res = res.append(temp,ignore_index = True)
df1 = df1.append(temp.iloc[:,:df1.shape[1]],ignore_index = True).drop_duplicates(keep = False)
temp = df1.merge(df2,'inner',left_on = '地址',right_on = '截取地址')
temp['匹配方式'] = '学区地址-小区地址'
temp['distance'] = 0.0
res = res.append(temp,ignore_index = True)
df1 = df1.append(temp.iloc[:,:df1.shape[1]],ignore_index = True).drop_duplicates(keep = False)


df1['key'] = 1
df2['key'] = 1
df = df1.merge(df2,on = 'key')
df['distance'] = np.sqrt( (df['纬度'] - df['高德纬度'])**2 + (df['经度'] - df['高德经度'])**2 )
temp = df.loc[df.groupby(['地址'])['distance'].idxmin()]
temp['匹配方式'] = '坐标'

res = res.append(temp.loc[:,res.columns],ignore_index = True)
res.to_clipboard()
