#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 15:22:30 2020

@author: adrian
"""
import os
import sorter
import sys
import json
import numpy as np

#folder=os.getcwd()
folder=sys.argv[1];
os.chdir(folder);

subfolders = [ f.path for f in os.scandir(folder) if f.is_dir() ]

#Order folders numerically
F=[f.split('_')[-1] for f in subfolders];
NF=F;
NF = [int(x) for x in NF]
NF.sort();
NF = [str(x) for x in NF]


ind=[];
for f in NF:
 ind.append(int(F.index(f)))

mylist = [subfolders[i] for i in ind]

#Look for json file. If there is no file then run consensus in all tetrodes.
try:
    print('Reading JSON')
    with open("run_consensus.json", 'r') as f:
        run_consensus = json.load(f)
        run_consensus=np.array(run_consensus);
except FileNotFoundError:
    #No file. We make all values ones.
    print('JSON not found. Please add JSON.')
    #run_consensus=np.ones(len(mylist), dtype=int);
    sys.exit()

counter=0;
for tetrode in mylist:
    if run_consensus[counter]== 1:
        print('Manual curation on consensus detections')
        sorter.manual_phy(tetrode)
    else:
        print('Manual curation on MS4 detections')
        sorter.manual_phy(tetrode)
    counter=counter+1;
