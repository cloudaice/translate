#!/usr/bin/env python
#-*-coding:utf-8-*-

#file: translate.py
#author: cloudaice
import urllib2 
import urllib
import json

class Youdao(object):
    def __init__(self):
        self.args = {'keyfrom':'cloudaice',
                     'key':'425760193',
                     'type':'data',
                     'doctype':'json',
                     'version':'1.1',
                     'q': None
                 }
        self.source_url = 'http://fanyi.youdao.com/openapi.do?' 
        self.url = None

    def set(self,q):
        self.args['q'] = q
        self.url = self.source_url + urllib.urlencode(self.args)
    
    def get(self):
        try:
            req = urllib2.Request(self.url)
            res = urllib2.urlopen(req)
            result = json.loads(res.read())
            return result['basic']['explains']
        except:
            print '网络错误'
            return None

if __name__ == "__main__":
    while True:
        translate = Youdao()
        query = raw_input("fy>")
        if query == 'q':
            exit()
        translate.set(query)
        result = translate.get()
        if not result:
            continue
        for v in result:
            print v
    
