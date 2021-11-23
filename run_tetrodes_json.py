#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 17:59:26 2021

@author: adrian
"""
import os
import sorter
import sys
import json
import numpy as np
import time
import shutil
brain_area=sys.argv[1];

#folder='/media/adrian/GL04_RAT_HOMER_2/Spike_sorting/Rat_OS_RGS14_Rat3_357152_SD1_OD_10-11_10_2019/Rat_OS_Ephys_RGS14_Rat3_357152_SD1_OD_10-11_10_2019_merged/hpc';
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/assembly/Cell_assembly/cortex';
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/Rat_OS_Ephys_RGS14_Rat2_57987_SD6_CON_04-05_08_2018/Rat_OS_Ephys_RGS14_Rat2_57987_SD6_CON_04-05_08_2018_merged/hpc';
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/Rat_OS_Ephys_RGS14_Rat4_357153_SD10_CON_29-30_11_2019/Rat_OS_Ephys_RGS14_Rat4_357153_SD10_CON_29-30_11_2019_merged/hpc';
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/Rat_OS_Ephys_RGS14_rat7_373727_SD10_OR_02-03_03_2020/Rat_OS_Ephys_RGS14_rat7_373727_SD10_OR_02-03_03_2020_merged/hpc'
#folder='/media/adrian/GL13_RAT_BURSTY/Rat_OS_Ephys_RGS14_rat4_357153/Rat_OS_Ephys_RGS14_Rat4_357153_SD10_CON_29-30_11_2019/merged/hpc';
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/Rat_OS_Ephys_RGS14_Rat3_357152_SD6_OR_21-22_10_2019_PT5_Test_merged/cortex';
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/Rat_OS_Ephys_RGS14_Rat3_357152_SD6_OR_21-22_10_2019_Test_merged/hpc'
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/OS_Ephys_RGS14_Rat8_378133_SD3_OR_27-28_04_2020/OS_Ephys_RGS14_Rat8_378133_SD3_OR_27-28_04_2020_merged/hpc';
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/OS_Ephys_RGS14_Rat8_378133_SD6_OD_04-05_05_2020/OS_Ephys_RGS14_Rat8_378133_SD6_OD_04-05_05_2020_merged/cortex';
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/OS_Ephys_RGS14_Rat8_378133_SD10_HC_15_05_2020/OS_Ephys_RGS14_Rat8_378133_SD10_HC_15_05_2020_Trial1_Post_Trial1_merged/hpc';
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/OS_Ephys_RGS14_Rat8_378133_SD10_HC_15_05_2020/OS_Ephys_RGS14_Rat8_378133_SD10_HC_15_05_2020_merged/hpc';
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/Rat_OS_Ephys_RGS14_Rat1_57986_SD4_HC_01_08_2018/Rat_OS_Ephys_RGS14_Rat1_57986_SD4_HC_01_08_2018_merged/cortex';
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/x/OS_Ephys_RGS14_Rat3_357152_SD5_CON_18-19_10_2019_merged/cortex';
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/Rat_OS_Ephys_RGS14_rat6_373726_SD1_HC_01_02_2020/Rat_OS_Ephys_RGS14_rat6_373726_SD1_HC_01_02_2020_merged/cortex';
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/OS_Ephys_RGS14_Rat8_378133_SD6_OD_04-05_05_2020_merged/hpc';
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/Rat_OS_Ephys_RGS14_rat6_373726_SD2_OR_06-07_02_2020/Rat_OS_Ephys_RGS14_rat6_373726_SD2_OR_06-07_02_2020_merged/hpc';
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/Rat_OS_Ephys_RGS14_rat6_373726_SD3_CON_11-12_02_2020/Rat_OS_Ephys_RGS14_rat6_373726_SD3_CON_11-12_02_2020_merged/cortex';
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/Rat_OS_Ephys_RGS14_rat7_373727_SD2_OR_03_04-02-2020/Rat_OS_Ephys_RGS14_rat7_373727_SD2_OR_03_04-02-2020_merged/cortex';
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/OS_Ephys_RGS14_Rat3_357152_SD5_CON_18-19_10_2019_error/OS_Ephys_RGS14_Rat3_357152_SD5_CON_18-19_10_2019_merged/'
folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/OS_Ephys_RGS14_Rat3_357152_SD5_CON_18-19_10_2019_error/OS_Ephys_RGS14_Rat3_357152_SD5_CON_18-19_10_2019'
original=folder+'_Trial1_Post_Trial1_merged/'+brain_area;
target = folder+'_merged/'+brain_area;


#folder=sys.argv[1];
os.chdir(original);

subfolders = [ f.path for f in os.scandir(original) if f.is_dir() ]

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


Original = original+'/run_consensus.json';
#target = r'target path where the file will be copied\file name.file extension'
Target = target+'/run_consensus.json';

shutil.copyfile(Original, Target)
