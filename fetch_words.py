#-*-coding: utf-8 -*-
import sys


if len(sys.argv) < 3:
    print 'no source file and out file'
    exit()
    

source_file = sys.argv[1]
out_file = sys.argv[2]
fd = open(source_file, 'r')
fd2 = open(out_file, 'w')
for line in fd.readlines():
    line = line.split('@')
    fd2.write('%s     %s' % (line[0], line[2]))
