# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 10:59:10 2021

@author: Peter
"""
from Function import Time
import requests
LunarKey='0d106ac4c2e99a388c5afd59b695cb01'#聚合数据_万年历
LunarURL='http://v.juhe.cn/calendar/day'
def getHoliday():
    Date=str(Time.getYear())+'-'+str(Time.getMonth())+'-'+str(Time.getDay())
    print(Date)
    try:
        result = requests.get(LunarURL, params={
            'key': LunarKey,
            'date': Date
        }, timeout=5)
        result = eval(result.text)  # 若请求结果为Resonse<200>，那么可以尝试.text来访问
        if len(result['result']['data']['holiday'])==0:
            print("c")
            return '无节日'
        else:
            result['result']['data']['holiday']
    except:
        print("b")
        return 0
Holiday=getHoliday()
print(Holiday)