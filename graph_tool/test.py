#!/usr/bin/env python

import os
import csv
import itertools
import graph_tool.all as gt

gIMUData = gt.Graph()

gIMUData.add_vertex(5)

myFileNameLoad="my.csv"
with open(myFileNameLoad, 'rb') as pageList:
        stateReader = csv.reader(pageList, delimiter=',', quotechar='"')
        #this is for the rows in your downloaded file
        start = 1
        end = 5
        for row in itertools.islice(stateReader, start, end):
	    print row[0]
	    gIMUData.add_vertex(int(row[0]))

vlist = list(gIMUData.add_vertex(5))
vlist2 = []
for v in gIMUData.vertices():
     vlist2.append(v)

print vlist
print gIMUData

assert(vlist == vlist2)


#help(gt.Graph)

