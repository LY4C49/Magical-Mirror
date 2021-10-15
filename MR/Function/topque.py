# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 14:38:23 2021

@author: Peter
"""

import urllib.request as ur
import re
def GetTopQue():
    url = "https://www.zhihu.com/api/v4/search/top_search"
    req = ur.Request(url)
    content= ur.urlopen(req, timeout=600).read().decode('utf-8')
    content= str(content)
    pattern=re.compile("\"display_query\":\"(.*?)\"")
    result=pattern.findall(content)
    return result
