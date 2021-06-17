#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 02:02:46 2021

@author: adrian
"""
import os
import sys
import numpy as np
from pathlib import Path
import math

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
    #outpath.mkdir(exist_ok=True)
    
    cont = sorted(basepath.glob("*.continuous"))
    
    #Move to next iteration if there are no .continuous files in folder
    if len(cont)==0:
        print('No .continuous files found')
        os.chdir("..")
        continue
    
    fsizes = [f.stat().st_size for f in cont]
    shortest, longest = min(fsizes), max(fsizes)
    #Find if there are length discrepancies.
    if shortest != longest:
        print("shortest:", shortest, "Bytes | longest:", longest, "Bytes")
        trunc_bytes = math.floor((shortest-1024)/2070)*2070+1024
        print(f"truncate to {trunc_bytes} bytes!")
        
        outpath.mkdir(exist_ok=True)
        for n, f in enumerate(cont):
            mm = np.memmap(f, mode="r", dtype=np.uint8)
            outfname = outpath / f.name
            print(f"Truncating {outfname.name} to {trunc_bytes} Bytes, cutting {fsizes[n]-trunc_bytes} Bytes")
            mm_out = np.memmap(outfname, mode="w+", shape=(trunc_bytes, ), dtype=np.uint8)
            mm_out[:] = mm[:trunc_bytes]
            del mm, mm_out
    else:
        print('No length issues detected')
    
    os.chdir("..")

os.chdir('/media/adrian/GL13_RAT_BURSTY/Rat_OS_Ephys_RGS14_rat4_357153/Rat_OS_Ephys_RGS14_Rat4_357153_SD10_CON_29-30_11_2019/2019-11-29_09-33-21_Pre-sleep')
basepath = Path(".").resolve()
outpath = basepath / "truncated"
#outpath.mkdir(exist_ok=True)

cont = sorted(basepath.glob("*.continuous"))
fsizes = [f.stat().st_size for f in cont]
shortest, longest = min(fsizes), max(fsizes)
if shortest != longest:
    print("shortest:", shortest, "Bytes | longest:", longest, "Bytes")
    trunc_bytes = math.floor((shortest-1024)/2070)*2070+1024
    print(f"truncate to {trunc_bytes} bytes!")
    
    outpath.mkdir(exist_ok=True)
    for n, f in enumerate(cont):
        mm = np.memmap(f, mode="r", dtype=np.uint8)
        outfname = outpath / f.name
        print(f"Truncating {outfname.name} to {trunc_bytes} Bytes, cutting {fsizes[n]-trunc_bytes} Bytes")
        mm_out = np.memmap(outfname, mode="w+", shape=(trunc_bytes, ), dtype=np.uint8)
        mm_out[:] = mm[:trunc_bytes]
        del mm, mm_out
