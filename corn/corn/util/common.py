'''
Created on Aug 11, 2017

@author: zhout
'''
import json

def httpResponseToDict(response):
    res_byte = response.read()
    res_txt = res_byte.decode('utf-8')
    return json.loads(res_txt)