# -*- coding:utf-8 -*-
import sys
import sqlite3

try:
    filename=sys.argv[1]
except IndexError:
    filename=raw_input("输入文件名称\n")
conn = sqlite3.connect('translate.db')
c = conn.cursor()
c.execute("select * from translate order by frequency desc")
export=''
f = open(filename,'w')
for row in c:
    for word in row:
        try:
            export+=("%s     " %word.encode('utf-8'))
        except AttributeError:
            export+=("%s      " %word)
    export+='\n'
f.write(export)
c.close()
    



