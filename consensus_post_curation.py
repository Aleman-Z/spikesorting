#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 13:22:30 2020

@author: adrian
"""


import sys
import os
import spikeinterface
import spikeinterface.extractors as se 
import spikeinterface.toolkit as st
import spikeinterface.sorters as ss
import spikeinterface.comparison as sc
import spikeinterface.widgets as sw
import matplotlib.pylab as plt
import numpy as np
import time 
import glob
import csv


#recording_folder=os.getcwd();
recording_folder=sys.argv[1];
os.chdir(recording_folder)


Sorters2Compare=[];
Sorters2CompareLabel=['KL','IC','Waveclus','HS','MS4','SC','TRI'];
Sorters2label=['KL','IC','Waveclus','HS','MS4','SC','TRI'];
subfolders = [ f.name for f in os.scandir(recording_folder) if f.is_dir() ];


for num in range(len(Sorters2CompareLabel)):
     i=Sorters2CompareLabel[num];
#     print(i)
     if 'phy_'+i in subfolders:
         sorting_curated = se.PhySortingExtractor('phy_'+i+'/', exclude_cluster_groups=['noise','mua']);
         if not sorting_curated.get_unit_ids():
             Sorters2label.remove(i)
         else:
                 Sorters2Compare.append(sorting_curated);
         

#Consensus based curation.
print(Sorters2label)
print('Comparing sorters agreement. Please wait...')
mcmp = sc.compare_multiple_sorters(Sorters2Compare, Sorters2label)
w = sw.plot_multicomp_agreement_by_sorter(mcmp)


plt.savefig('consensus_curation.pdf', bbox_inches='tight');
plt.savefig('consensus_curation.png', bbox_inches='tight');
plt.close()

w = sw.plot_multicomp_agreement(mcmp)
plt.savefig('consensus_curation_spikes.pdf', bbox_inches='tight');
plt.savefig('consensus_curation_spikes.png', bbox_inches='tight');
plt.close()

    
print('Consensus ended. Results saved')

