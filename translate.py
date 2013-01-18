#!/usr/bin/env python
#-*-coding:utf-8-*-

#file: translate.py
#author: cloudaice

import urllib2 
import urllib
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

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

def save_words(words_dict):
    fd = open('words.db','w')
    for word in words_dict:
        line = []
        line.append(word)
        line.append(words_dict[word]['means'])
        line.append(str(words_dict[word]['times']))
        fd.write('@'.join(line) + '\n')                #每个单词之间采用@号分隔
    fd.close()

if __name__ == "__main__":
    words_dict = {}
    fd = open('words.db','r')
    for line in fd.readlines():
        line = line.split('@')
        words_dict[line[0]] = {}
        words_dict[line[0]]['means'] = line[1]
        words_dict[line[0]]['times'] = int(line[2])

    while True:
        translate = Youdao()
        query = raw_input("fy>")
        if query == 'q':
            exit()
        if query == '':
            continue
        if query in words_dict:
            words_dict[query]['times'] += 1
            print '\n'.join(words_dict[query]['means'].split('#'))
            save_words(words_dict)
            continue
        translate.set(query)
        result = translate.get()
        if not result:
            continue
        for v in result:
            print v
        result = '#'.join(result)           #释义行与行之间采用#号分隔
        words_dict[query] = {}
        words_dict[query]['times'] = 1
        words_dict[query]['means'] = result
        save_words(words_dict)
