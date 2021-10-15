# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 11:39:46 2021

@author: Peter
"""
import urllib.request as ur
import re 


def Getname():
    file=open('name.txt','r')
    name=file.readline()
    return name

def GetURL(name):
    url=""
    if name=="LLY":
        url="http://47.94.219.117/welcome-lly/"
        
    if name=="Yann":
        url="http://47.94.219.117/welcome-yann/"
        
    if name=="ZCR":
        url="http://47.94.219.117/welcome-zcr/"
    
    if name=="horse":
        url="http://47.94.219.117/welcome-horse/"
    return url
        
def GetAgenda(url):
    req = ur.Request(url)
    html1 = ur.urlopen(req, timeout=600).read().decode('utf-8')
    html1 = str(html1)

    pattern=re.compile("<li>(.*?)</li")
    result=pattern.findall(html1)

    blacklist="http"
    result_pure=[]

    for item in result:
        if blacklist not in item:
            result_pure.append(item)
    return result_pure
