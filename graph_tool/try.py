#!/usr/bin/env python

import os
import csv
import itertools
import graph_tool.all as gt

g = gt.Graph()
vlist = list(g.add_vertex(5))
vlist2 = []
for v in g.vertices():
     vlist2.append(v)

assert(vlist == vlist2)
#help(gt.Graph)

#print vlist

#print g

myFileNameLoad="my.csv"
with open(myFileNameLoad, 'rb') as pageList:
        stateReader = csv.reader(pageList, delimiter=',', quotechar='"')
        #this is for the rows in your downloaded file
        start = 2
        end = 3
        for row in itertools.islice(stateReader, start, end):
            if row[9] == "PA":
                print row[9]  + " is california"
                #print str(listLoad[x]) + " is california"
            else:
                #print str(listLoad[x]) + " is NOT CALIFORNIA!!!!!!!!!"
                print row[9]
