#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 18:37:52 2020

@author: adrian
"""
import os
import sorter
import sys
import json
import numpy as np
import time

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
    print('JSON not found. Running consensus in all tetrodes')
    run_consensus=np.ones(len(mylist), dtype=int);

counter=0;
for tetrode in mylist:
    start = time.time()

    if run_consensus[counter]== 1:
        sorter.auto(tetrode)
    else:
        sorter.ms4(tetrode)
    counter=counter+1;

    end = time.time()
    print(end - start)
    
