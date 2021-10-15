# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 11:19:37 2021

@author: Peter
"""
import requests
def getHot():#获取百度热搜前三
    newsList = requests.get('http://top.baidu.com/mobile_v2/buzz/hotspot/')
    newsList=eval(newsList.text)
    top3=[]
    for i in range(0,3):
        top3.append(newsList['result']['topwords'][i]['keyword'])
    return top3
hot=[]
hot=getHot()
print(hot)