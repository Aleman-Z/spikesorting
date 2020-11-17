#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 15:22:30 2020

@author: adrian
"""
import os
import sorter
import sys

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

for tetrode in mylist:
    sorter.manual(tetrode)