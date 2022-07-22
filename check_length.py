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
#Check if there are merged folders already.
merged_folders = [s for s in subdirectories if "merged" in s]

#Only run if merging has not be run before.
if len(merged_folders)==0:
    
    for s in subdirectories:
        os.chdir(s)
        print(s)
    
        #os.chdir('/media/adrian/GL13_RAT_BURSTY/Rat_OS_Ephys_RGS14_rat4_357153/Rat_OS_Ephys_RGS14_Rat4_357153_SD10_CON_29-30_11_2019/2019-11-29_09-33-21_Pre-sleep')
        basepath = Path(".").resolve()
        outpath = basepath / "truncated"
        #outpath.mkdir(exist_ok=True)
        
        #cont = sorted(basepath.glob("*CH*"))
        cont=sorted( set(sorted(basepath.glob("*CH*"))) -set(sorted(basepath.glob("*.mat*")))-set(sorted(basepath.glob("*.recons*"))))
        cont_aux=sorted( set(sorted(basepath.glob("*AUX*"))) - set(sorted(basepath.glob("*recons*")))); #To not include recons files.
        cont_all=cont+cont_aux;
        #cont_str=[str(f) for f in cont];
        
        
        #Move to next iteration if there are no .continuous files in folder
        if len(cont)==0:
            print('No .continuous files found')
            os.chdir("..")
            continue
        
        if len(cont_aux)!=6 & len(cont_aux)!=0:
            print ('Warning: The recording is likely split in chunks. Using largest chunk.')
            fsizes = [f.stat().st_size for f in cont_all]
            shortest, longest = min(fsizes), max(fsizes)
            #Finding chunk with the longest duration
            y=1*np.array([f==longest for f in fsizes], dtype=int)
            y_ind=np.where(y);
            cont2=[cont_all[i] for i in y_ind[0]];
            outpath.mkdir(exist_ok=True)
            for n, f in enumerate(cont2):
                mm = np.memmap(f, mode="r", dtype=np.uint8)
                outfname = outpath / f.name
                print(f"Selecting {outfname.name} as largest chunk. Saving in 'truncated'.")
                mm_out = np.memmap(outfname, mode="w+",shape=(longest, ), dtype=np.uint8)
                mm_out[:] = mm;
                del mm, mm_out        
            os.chdir("..")
    
    
    
        else:
            fsizes = [f.stat().st_size for f in cont_all]
            shortest, longest = min(fsizes), max(fsizes)
            #Find if there are length discrepancies.
            if shortest != longest:
                print("shortest:", shortest, "Bytes | longest:", longest, "Bytes")
                trunc_bytes = math.floor((shortest-1024)/2070)*2070+1024
                print(f"truncate to {trunc_bytes} bytes!")
                
                outpath.mkdir(exist_ok=True)
                for n, f in enumerate(cont_all):
                    mm = np.memmap(f, mode="r", dtype=np.uint8)
                    outfname = outpath / f.name
                    print(f"Truncating {outfname.name} to {trunc_bytes} Bytes, cutting {fsizes[n]-trunc_bytes} Bytes")
                    mm_out = np.memmap(outfname, mode="w+", shape=(trunc_bytes, ), dtype=np.uint8)
                    mm_out[:] = mm[:trunc_bytes]
                    del mm, mm_out
            else:
                print('No length issues detected')
            
            os.chdir("..")
            
else:
    print('Merged folder already detected. You should only run this before merging.')

#os.chdir('/media/adrian/GL13_RAT_BURSTY/Rat_OS_Ephys_RGS14_rat4_357153/Rat_OS_Ephys_RGS14_Rat4_357153_SD10_CON_29-30_11_2019/2019-11-29_09-33-21_Pre-sleep')
#basepath = Path(".").resolve()
#outpath = basepath / "truncated"
##outpath.mkdir(exist_ok=True)

#cont = sorted(basepath.glob("*.continuous"))
#fsizes = [f.stat().st_size for f in cont]
#shortest, longest = min(fsizes), max(fsizes)
#if shortest != longest:
#    print("shortest:", shortest, "Bytes | longest:", longest, "Bytes")
#    trunc_bytes = math.floor((shortest-1024)/2070)*2070+1024
#    print(f"truncate to {trunc_bytes} bytes!")
    
#    outpath.mkdir(exist_ok=True)
#    for n, f in enumerate(cont):
#        mm = np.memmap(f, mode="r", dtype=np.uint8)
#        outfname = outpath / f.name
#        print(f"Truncating {outfname.name} to {trunc_bytes} Bytes, cutting {fsizes[n]-trunc_bytes} Bytes")
#        mm_out = np.memmap(outfname, mode="w+", shape=(trunc_bytes, ), dtype=np.uint8)
#        mm_out[:] = mm[:trunc_bytes]
#        del mm, mm_out
