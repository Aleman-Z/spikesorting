#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 16:35:47 2021

@author: adrian
"""

import os
import sorter
import sys
import json
import numpy as np
import time

#folder='/media/adrian/GL04_RAT_HOMER_2/Spike_sorting/Rat_OS_RGS14_Rat3_357152_SD1_OD_10-11_10_2019/Rat_OS_Ephys_RGS14_Rat3_357152_SD1_OD_10-11_10_2019_merged/hpc';
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/assembly/Cell_assembly/cortex';
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/Rat_OS_Ephys_RGS14_Rat2_57987_SD6_CON_04-05_08_2018/Rat_OS_Ephys_RGS14_Rat2_57987_SD6_CON_04-05_08_2018_merged/hpc';
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/Rat_OS_Ephys_RGS14_Rat4_357153_SD10_CON_29-30_11_2019/Rat_OS_Ephys_RGS14_Rat4_357153_SD10_CON_29-30_11_2019_merged/hpc'
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/Rat_OS_Ephys_RGS14_rat7_373727_SD10_OR_02-03_03_2020/Rat_OS_Ephys_RGS14_rat7_373727_SD10_OR_02-03_03_2020_merged/hpc'
Folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/Rat_OS_Ephys_RGS14_rat7_373727_SD10_OR_02-03_03_2020/Rat_OS_Ephys_RGS14_rat7_373727_SD10_OR_02-03_03_2020';
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/Rat_OS_Ephys_RGS14_rat7_373727_SD10_OR_02-03_03_2020/Rat_OS_Ephys_RGS14_rat7_373727_SD10_OR_02-03_03_2020_merged/'
#/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/Rat_OS_Ephys_RGS14_rat7_373727_SD10_OR_02-03_03_2020/Rat_OS_Ephys_RGS14_rat7_373727_SD10_OR_02-03_03_2020_Trial1_Post_Trial1_merged
str1='_Trial1_Post_Trial1_merged/cortex';
str2='_Trial1_Post_Trial1_merged/hpc';
str3='_merged/cortex';
str4='_merged/hpc';
STR=[str1,str2,str3,str4];

for i in range(4):
    if i==2:
        print(STR[i])
        print('create Json')
        asdf
        
    folder= Folder+STR[i]
    
    #folder=sys.argv[1];
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
        
