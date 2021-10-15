# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 14:22:34 2021

@author: Peter
"""
import requests
url='http://v.juhe.cn/calendar/day?date=2015-1-1&key=http://v.juhe.cn/calendar/day'

result=requests.get(url)
print(result)