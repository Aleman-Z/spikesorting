#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 13:12:32 2021

@author: adrian
"""
import numpy as np
from pathlib import Path
import math
import os
import sys
from shutil import copy2


folder=sys.argv[1];
#folder='/media/adrian/GL13_RAT_BURSTY/Rat_OS_Ephys_RGS14_rat4_357153/Rat_OS_Ephys_RGS14_Rat4_357153_SD10_CON_29-30_11_2019'
#os.chdir('/media/adrian/GL13_RAT_BURSTY/Rat_OS_Ephys_RGS14_rat4_357153/Rat_OS_Ephys_RGS14_Rat4_357153_SD10_CON_29-30_11_2019')
os.chdir(folder)

subdirectories=next(os.walk('.'))[1]
for s in subdirectories:
    os.chdir(s)
    print(s)

    #os.chdir('/media/adrian/GL13_RAT_BURSTY/Rat_OS_Ephys_RGS14_rat4_357153/Rat_OS_Ephys_RGS14_Rat4_357153_SD10_CON_29-30_11_2019/2019-11-29_09-33-21_Pre-sleep')
    basepath = Path(".").resolve()
    outpath = basepath / "truncated"
    outpath2 = basepath / "original"

    #outpath.mkdir(exist_ok=True)

    #Move to next iteration if there are no .continuous files in folder
    if outpath2.exists()== True:
        print('Tetrode was already truncated.')
        os.chdir("..")
        continue
   
    cont = sorted(basepath.glob("*.continuous"))
   
    fsizes = [f.stat().st_size for f in cont]
    shortest, longest = min(fsizes), max(fsizes)
    #Find if there are length discrepancies.
    if shortest != longest:
        print("Channels have different lengths. Check the issue.")
        exit()


    trunc_bytes = math.floor((shortest-1024)/2070)*2070+1024
        
        
    outpath.mkdir(exist_ok=True)
    for n, f in enumerate(cont):
        mm = np.memmap(f, mode="r", dtype=np.uint8)
        outfname = outpath / f.name
        print(f"Truncating {outfname.name} to {trunc_bytes} Bytes, cutting {fsizes[n]-trunc_bytes} Bytes")
        mm_out = np.memmap(outfname, mode="w+", shape=(trunc_bytes, ), dtype=np.uint8)
        mm_out[:] = mm[:trunc_bytes]
        del mm, mm_out
    
    outpath2.mkdir(exist_ok=True)
    
    for x in cont:
        copy2(x,outpath2)
        os.remove(x)
    
    # if shortest != longest:
    #     os.chdir(basepath / 'truncated_mismatch')
    # else:
    #     os.chdir(basepath / 'truncated')
                
    basepath2 = Path(".").resolve()
    cont = sorted(basepath2.glob("*.continuous"))
    for x in cont:
        copy2(x,basepath)
        os.remove(x)
    
    

    os.chdir("..")

    os.chdir("..")
