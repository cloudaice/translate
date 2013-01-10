#-*-coding:utf-8-*-
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
            req = urllib2.Request(url)
            res = urllib2.urlopen(req)
        except:
            pass
        result = res.read()
        try:
            result = json.loads(result)
        except:
            pass
            

for v in result['basic']['explains']:
    print v
for arg in result['web']:
    print arg['key']
    for v in  arg['value']:
        print v

while True:
    translate = Youdao()
    query = raw_input("fy>")
    translate.set(query)
    result = translate.get()
    print result
    
