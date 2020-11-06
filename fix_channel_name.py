#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 16:43:45 2020

@author: adrian
"""
import os

folderpath='/home/adrian/Documents/SpikeSorting/Adrian_test_data/Irene_data/test_without_zero_main_channels/Tetrode_9';



source = '100';
chprefix = 'CH';
session = '_0'   ;

[source + '_'+chprefix + x + '.continuous' for x in map(str,channels)]


channels=op._get_sorted_channels(folderpath, chprefix, session,9);



os.listdir(folderpath)
Files = [f for f in os.listdir(folderpath) if '.continuous' in f
                                               and '_'+chprefix in f
                                               and source in f]

if session == '0':
    Files = [f for f in Files if len(f.split('_')) == 3]
    NF=[f.split('_0')[0]+f.split('_0')[1] for f in Files];
    for (f,nf) in zip(Files,NF):
            print(f, nf)
            os.rename(f, nf)

  