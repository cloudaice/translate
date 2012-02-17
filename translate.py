#coding=utf-8 
# trans.py   
# create :2010-6-2  
# last modify: 2010-6-3  
# author : ice_cube  
import sqlite3  
import urllib,urllib2    
from sgmllib import SGMLParser
import re
import time
  
class URLLister(SGMLParser):    
    """ 
    页面分析 
    """  
    def reset(self):    
        SGMLParser.reset(self)    
        self.result = []    
        self.open = False   
  
    def start_span(self, attrs):    
        id = [v for k, v in attrs if k=='id']    
        if 'result_box' in id:    
            self.open = True   
              
    def handle_data(self, text):    
        if self.open:    
            self.result.append(text)    
            self.open = False   
  
class GoogleTranslate(object):  
    def __init__(self):  
        self.url = 'http://translate.google.cn/translate_t'   
  
    def en2zh(self, text):  
        """从英文翻译到中文  text为要翻译的内容"""  
        values={'hl':'zh-CN','ie':'utf8','text':text,'langpair':"en|zh-CN"}    
        result = self.get_result(values)  
        return result  
  
    def zh2en(self, text):  
        """从中文翻译到英文  text为要翻译的内容"""  
        values={'hl':'zh-CN','ie':'utf8','text':text,'langpair':"zh-CN|en"}    
        result = self.get_result(values)  
        return result  
  
    def get_result(self, values):  
        result = ""  
        data = urllib.urlencode(values)    
        req = urllib2.Request(self.url, data)    
        req.add_header('User-Agent', "Mozilla/5.0+(compatible;+Googleb/2.1;++http://www.google.com/bot.html)")    
        response = urllib2.urlopen(req)    
        parser = URLLister()    
        parser.feed(response.read())    
        parser.close()    
        for i in parser.result:    
            result += i + " "  
        return result  

def outdata(text,conn,c):
    print "正在网络翻译..."
    zh = trans.en2zh(text)
    en = trans.zh2en(text)
    zh = ' '.join(zh.split())
    en = ' '.join(en.split())
    if zh == en :
        print "无法翻译..."
    else:
        date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        query = "insert into translate values('%s','%s','%s',%d)" %(date,en.lower(),zh.lower(),0)
        c.execute(query)
        conn.commit()
        print "翻译结果:"
        print "中文：",zh
        print "英文：",en

def is_en(text):
    m=re.match('[A-Za-z ]*',text)
    if not m:
        return 'zh'
    else:
        if m.group()==text:
            return 'en'
        else:
            if ''.join(m.group().split())=='':
                return 'zh'
            else:
                return None 

    
if __name__ == "__main__":  
    trans = GoogleTranslate()  
    while True:    
        conn=sqlite3.connect('translate.db')
        c=conn.cursor()
        text = raw_input("请输入要翻译的英文(退出输入q)：")    
        text= ' '.join(text.split())
        if text=='q':    
            c.close()  
            break;      
        if is_en(text)=='en':
            '''如果是英 文检索数据库'''
            query=("select chinese from translate where english ='%s'" %text.lower())
            c.execute(query)
            result = c.fetchall()
            if not result: 
                outdata(text,conn,c)
            else:
                query=("update translate set frequency = frequency+1 where english ='%s'" %text.lower())
                c=conn.cursor()
                c.execute(query)
                conn.commit()
                print " 翻译结果e:"
                print "中文:",result[0][0]
                print "英文:",text
                

        elif is_en(text)=='zh':
            '''如果是中文检索数据库'''
            query= ("select english from translate where chinese = '%s'" %text)
            c.execute(query)
            conn.commit()
            result = c.fetchall()
            if not result:
                outdata(text,conn,c)
            else:
                query=("update translate set frequency = frequency+1 where chinese ='%s'" %text)
                c=conn.cursor()
                c.execute(query)
                conn.commit()
                print "翻译结果z:"
                print "中文:",text
                print "英文:",result[0][0]
        else:
            print "正在网络翻译..."
            print "翻译结果:"
            print "中文：",trans.en2zh(text)
            print "英文：",trans.zh2en(text)
         
