#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 15:52:12 2021

@author: adrian
"""
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
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/OS_Ephys_RGS14_Rat3_357152_SD5_CON_18-19_10_2019_error/OS_Ephys_RGS14_Rat3_357152_SD5_CON_18-19_10_2019'
#folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/Rat_OS_Ephys_RGS14_Rat1_57986_SD4_HC_01_08_2018_error/Rat_OS_Ephys_RGS14_Rat1_57986_SD4_HC_01_08_2018';
folder='/media/adrian/6aa1794c-0320-4096-a7df-00ab0ba946dc/spike_soting/Rat_OS_Ephys_RGS14_Rat1_57986_SD5_CON_02-03_08_2018/Rat_OS_Ephys_RGS14_Rat1_57986_SD5_CON_02-03_08_2018';
folder=folder+brain_area;

#folder=sys.argv[1];
os.chdir(folder);
try:
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
except:  
    #os.system('echo hi')
    exit()
    #os.system('python -m truncate2 '+ folder)