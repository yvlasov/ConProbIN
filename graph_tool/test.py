#!/usr/bin/env python

import os
import csv
import itertools
import graph_tool.all as gt

from graph_tool.all import *

gIMUData = gt.Graph()
vPropDOF1=gIMUData.vertex_properties["DOF1"] = gIMUData.new_vertex_property("int")
ePropDOF1=gIMUData.edge_properties["DOF1"] = gIMUData.new_edge_property("int")
myFileNameLoad="my.csv"

with open(myFileNameLoad, 'rb') as pageList:
        stateReader = csv.reader(pageList, delimiter=',', quotechar='"')
        start = 0
        end = 5
	curVrtx=-1
        for row in itertools.islice(stateReader, start, end):
	    prevVrtx=curVrtx
	    print row[0]
	    curVrtx=gIMUData.add_vertex(1)
	    vPropDOF1[curVrtx] = int(row[0])
	    if prevVrtx !=-1:
		curEdge=gIMUData.add_edge(prevVrtx,curVrtx)
		ePropDOF1[curEdge] = int(row[0]) - vPropDOF1[prevVrtx]

print gIMUData.list_properties()
print gIMUData
#myVertx=gIMUData.vertex(0,use_index=False)

for eachVrtx in gIMUData.vertices():
    print vPropDOF1[eachVrtx]
    for eachEdg in eachVrtx.all_edges():
	print eachEdg
gIMUData.add_edge(gIMUData.vertex(0),gIMUData.vertex(4))

graph_draw(gIMUData, edge_text=ePropDOF1 ,vertex_text=vPropDOF1, edge_font_size=24, vertex_font_size=18, output_size=(600, 600), output="two-nodes.png")
