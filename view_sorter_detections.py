#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 11:56:29 2020

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
from shutil import rmtree

#Folder with tetrode data
#recording_folder='/home/adrian/Documents/SpikeSorting/Adrian_test_data/Irene_data/test_without_zero_main_channels/Tetrode_9_CH';
recording_folder=os.getcwd()
os.chdir(recording_folder)

"""
Adding Matlab-based sorters to path

"""
iron_path = "~/Documents/SpikeSorting/ironclust";

#IronClust
ss.IronClustSorter.set_ironclust_path(os.path.expanduser(iron_path))
ss.IronClustSorter.ironclust_path

# #HDSort
# ss.HDSortSorter.set_hdsort_path('/home/adrian/Documents/SpikeSorting/HDsort')
# ss.HDSortSorter.hdsort_path

# #Waveclus
# ss.WaveClusSorter.set_waveclus_path('/home/adrian/Documents/SpikeSorting/wave_clus')
# ss.WaveClusSorter.waveclus_path

#Check if the recording has been preprocessed before and load it.
# Else proceed with preprocessing.
arr = os.listdir()
        
#Load .continuous files 
recording = se.OpenEphysRecordingExtractor(recording_folder) 
channel_ids = recording.get_channel_ids() 
fs = recording.get_sampling_frequency()
num_chan = recording.get_num_channels()


print('Channel ids:', channel_ids)
print('Sampling frequency:', fs)
print('Number of channels:', num_chan)


#!cat tetrode9.prb #Asks for prb file
# os.system('cat /home/adrian/Documents/SpikeSorting/Adrian_test_data/Irene_data/test_without_zero_main_channels/Tetrode_9_CH/tetrode9.prb') 
recording_prb = recording.load_probe_file('tetrode.prb')

print('Channels after loading the probe file:', recording_prb.get_channel_ids())
print('Channel groups after loading the probe file:', recording_prb.get_channel_groups())

#For testing only: Reduce recording.
#recording_prb = se.SubRecordingExtractor(recording_prb, start_frame=100*fs, end_frame=420*fs)


#Bandpass filter 
recording_cmr = st.preprocessing.bandpass_filter(recording_prb, freq_min=300, freq_max=6000)
recording_cache = se.CacheRecordingExtractor(recording_cmr) 

print(recording_cache.get_channel_ids())
print(recording_cache.get_channel_groups())
print(recording_cache.get_num_frames() / recording_cache.get_sampling_frequency())

#%%
#sorting_mountainsort4_all = ss.run_mountainsort4(recording_cache, output_folder='results_all_mountainsort4',delete_output_folder=True, filter=False)
#sorting_mountainsort4_all=se.NwbSortingExtractor('sorting_mountainsort4_all.nwb');

#st.postprocessing.export_to_phy(recording_cache, 
                                sorting_mountainsort4_all, output_folder='phy_MS4',
                                grouping_property='group', verbose=True, recompute_info=True)
#%%
sorting_check = se.PhySortingExtractor('phy_AGR/')

st.postprocessing.export_to_phy(recording_cache, 
                                sorting_check, output_folder='phy_check',
                                grouping_property='group', verbose=True, recompute_info=True)

os.system('phy template-gui phy_check/params.py')
