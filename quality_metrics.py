"""
Created on Fri Nov 12 15:33:06 2021

@author: Dimitris Exarchou
"""

## Import libraries and modules
import os
import re
import pickle
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import spikeinterface
import spikeinterface.extractors as se 
import spikeinterface.toolkit as st
import spikeinterface.sorters as ss
import spikeinterface.comparison as sc
import spikeinterface.widgets as sw


## Define paths
# base_dir   = '/media/genzel/Data/Dimitris_merging/OS_Ephys_RGS14_Rat3_357152_SD14_HC_16-11-2019_merged'
# areas = ['cortex', 'hpc']
base_dir   = '/mnt/genzel/Rat/OS/OS_rat_ephys/spikesorting/Rat_OS_Ephys_Rat9_57989_SD14_OR_SD_NOV_23-24_05_2018_merged'
areas = ['cortex'] # We have only cortex sortings


# Sorting functions
def atof(text):
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval

def natural_keys(text):
    return [ atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text) ]


## Compute quality metrics
for i in range(len(areas)):

    area_path = os.path.join(base_dir, areas[i])

    subdirs = [subdir for subdir in os.listdir(area_path) if os.path.isdir(os.path.join(area_path, subdir))]
    subdirs.sort(key=natural_keys)
    #subdirs = subdirs[6:] # continue from tetrode 6
    
    for j in range(len(subdirs)):
    
        rec_path = os.path.join(area_path, subdirs[j])
        phy_path = [subdir for subdir in os.listdir(rec_path) if os.path.isdir(os.path.join(rec_path, subdir)) and 'phy' in subdir][0]
        phy_path = os.path.join(rec_path, phy_path)
        
        print('~'*110 + '\n' + rec_path + '\n' + '~'*110)
        
        # Check if the quality metrics for this tetrode where previously calculated
        arr = os.listdir(base_dir)
        flag = 0
        
        for f in arr:
            if subdirs[j] in f:
                print("Skipping Tetrode...")
                flag = 1
                break
        
        if flag == 1:
            continue
        
        # Load recording extractor
        print('Loading Recording Extractor...')
        recording = se.OpenEphysRecordingExtractor(rec_path)
        # recording_prb = recording.load_probe_file(os.path.join(base_dir, 'tetrode.prb'))
        # print('Channels after loading the probe file:', recording_prb.get_channel_ids())
        # print('Channel groups after loading the probe file:', recording_prb.get_channel_groups())
	   
        # Load sorting extractor
        print('Loading Phy Sorting Extractor...')
        sorting = se.PhySortingExtractor(phy_path, exclude_cluster_groups=['noise'])
            
        print('Units:', len(sorting.get_unit_ids()))
        # print('Spikes of first unit:', len(sorting.get_unit_spike_train(1)))
        # print('Shared properties:', sorting.get_shared_unit_property_names())
        
        # Get waveforms
        # waveforms = st.postprocessing.get_unit_waveforms(recording, sorting, verbose=True)

        # Calculate quality metrics
        quality_metrics = st.validation.compute_quality_metrics(sorting, recording, 
                                                                metric_names=['isi_violation', 'snr', 'l_ratio'], 
                                                                as_dataframe=True)
        # display(quality_metrics)
        excel_name = '/quality_metrics_' + subdirs[j] + '.xlsx'
        quality_metrics.to_excel(base_dir + excel_name) 




## Merge excel files
print('Merging excel files...')
filenames = os.listdir(base_dir)
filenames_filtered = []

for i in range(len(filenames)):
    if 'Tetrode' in filenames[i] and '.xlsx' in filenames[i]: 
        filenames_filtered.append(filenames[i])
    
filenames_filtered.sort(key=natural_keys)

for filename in filenames_filtered:
    print(filename)

# Load excels as dataframes
df_list = []

for filename in filenames_filtered:  
    df_list.append(pd.read_excel(os.path.join(base_dir, filename), sheet_name='Sheet1', index_col=[0]))
    
# Create a merged dataframe
pieces = {}

for i in range(len(filenames_filtered)):
    filename = filenames_filtered[i]
    tetrode = filename.split('metrics_')[1]
    tetrode = tetrode.split('.')[0]
    pieces[tetrode] = df_list[i]
    
result = pd.concat(pieces)

# Save output to a new excel file
excel_name = '/quality_metrics_merged.xlsx'
result.to_excel(base_dir + excel_name)    

# Delete previous xlsx files
for filename in filenames_filtered: 
    os.remove(os.path.join(base_dir, filename))

print('Deleted previous xlsx files!')




# =============================================================================
# 
# # Phy interface
# %%capture --no-display
# !phy template-gui /home/genzel/Desktop/OS_Ephys_RGS14_Rat3_357152_SD14_HC_16-11-2019_merged/hpc/Tetrode_1/phy_MS4/params.py
# 
# =============================================================================


