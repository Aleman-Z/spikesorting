#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 01:54:36 2020

@author: adrian
"""
import os
import sys
# import numpy as np
import json

#folder=os.getcwd()
folder=sys.argv[1];

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

run_consensus=[];
for tetrode in mylist:
    os.chdir(tetrode)
    subfolders_tetrode = [ f.name for f in os.scandir(tetrode) if f.is_dir() ]
    
    if 'phy_AGR' in subfolders_tetrode:
        run_consensus.append(1);
    else :
        run_consensus.append(0);
os.chdir("..") 
# run_consensus=np.array(run_consensus); 
# np.save('run_consensus', run_consensus) 

#Save file
with open("run_consensus.json", 'w') as f:
    # indent=2 is not needed but makes the file 
    # human-readable for more complicated data
    json.dump(run_consensus, f, indent=2)      
print('Json file created!')