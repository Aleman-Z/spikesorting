#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 16:43:45 2020

@author: adrian
"""
import os
import sys

folderpath=sys.argv[1];
os.chdir(folderpath)

#Find .continuous files
source = '100';
chprefix = 'CH';

Files = [f for f in os.listdir(folderpath) if '.continuous' in f
                                               and '_'+chprefix in f
                                               and source in f]
#Previous name
Files = [f for f in Files if len(f.split('_')) == 3]
#New name
NF=[f.split('_0')[0]+f.split('_0')[1] for f in Files];
#Rename
for (f,nf) in zip(Files,NF):
        print(f, nf)
        os.rename(f, nf)

#Aux channels
chprefix = 'AUX';

Files = [f for f in os.listdir(folderpath) if '.continuous' in f
                                               and '_'+chprefix in f
                                               and source in f]
#Previous name
Files = [f for f in Files if len(f.split('_')) == 3]
#New name
NF=[f.split('_0')[0]+f.split('_0')[1] for f in Files];
#Rename
for (f,nf) in zip(Files,NF):
        print(f, nf)
        os.rename(f, nf)