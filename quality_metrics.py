"""
Created on Fri Nov 12 15:33:06 2021

@author: Dimitris Exarchou
"""

# Import libraries and modules
import os
import re
import pickle
import numpy as np
import matplotlib.pylab as plt
import spikeinterface
import spikeinterface.extractors as se 
import spikeinterface.toolkit as st
import spikeinterface.sorters as ss
import spikeinterface.comparison as sc
import spikeinterface.widgets as sw


# Define paths
output_dir = '/home/genzel/dimitris/quality_metrics/rat9_sd14'
base_dir   = '/mnt/genzel/Rat/OS/OS_rat_ephys/spikesorting/Rat_OS_Ephys_Rat9_57989_SD14_OR_SD_NOV_23-24_05_2018_merged'
# areas = ['cortex', 'hpc']
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


# Compute quality metrics
for i in range(len(areas)):

    area_path = os.path.join(base_dir, areas[i])

    subdirs = [subdir for subdir in os.listdir(area_path) if os.path.isdir(os.path.join(area_path, subdir))]
    subdirs.sort(key=natural_keys)
    #subdirs = subdirs[6:] # continue from tetrode 6
    
    for j in range(len(subdirs)):
    
        rec_path = os.path.join(area_path, subdirs[j])
        phy_path = [subdir for subdir in os.listdir(rec_path) if os.path.isdir(os.path.join(rec_path, subdir)) and 'phy' in subdir][0]
        phy_path = os.path.join(rec_path, phy_path)
        
        print('~'*60 + '\n' + rec_path + '\n' + '~'*60)
        
        # Check if the quality metrics for this tetrode where previously calculated
        arr = os.listdir(output_dir)
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
                                                                metric_names=['isi_violation', 'snr'], #, 'l_ratio'], 
                                                                as_dataframe=True)
        # display(quality_metrics)
        excel_name = '/quality_metrics_' + areas[i] + '_' + subdirs[j] + '.xlsx'
        quality_metrics.to_excel(output_dir + excel_name) 



# =============================================================================
# 
# # Phy interface
# %%capture --no-display
# !phy template-gui /home/genzel/Desktop/OS_Ephys_RGS14_Rat3_357152_SD14_HC_16-11-2019_merged/hpc/Tetrode_1/phy_MS4/params.py
# 
# 
# =============================================================================



# =============================================================================
# # Min ISI Tetrode 5 - Unit 0 
# %%capture --no-display
# !phy template-gui /home/genzel/Desktop/OS_Ephys_RGS14_Rat3_357152_SD14_HC_16-11-2019_merged/hpc/Tetrode_5/phy_AGR/params.py
# 
# 
# 
# # Max ISI Tetrode 11 - Unit 6
# %%capture --no-display
# !phy template-gui /home/genzel/Desktop/OS_Ephys_RGS14_Rat3_357152_SD14_HC_16-11-2019_merged/cortex/Tetrode_11/phy_AGR/params.py
# 
# 
# # Min SNR Tetrode 6 - Unit 3
# %%capture --no-display
# !phy template-gui /home/genzel/Desktop/OS_Ephys_RGS14_Rat3_357152_SD14_HC_16-11-2019_merged/cortex/Tetrode_6/phy_MS4/params.py
# 
# # Max SNR Tetrode 12 - Unit 15
# %%capture --no-display
# !phy template-gui /home/genzel/Desktop/OS_Ephys_RGS14_Rat3_357152_SD14_HC_16-11-2019_merged/cortex/Tetrode_12/phy_AGR/params.py
# 
# 
# 
# # Min L-ratio Tetrode 12 - Unit 0
# %%capture --no-display
# !phy template-gui /home/genzel/Desktop/OS_Ephys_RGS14_Rat3_357152_SD14_HC_16-11-2019_merged/cortex/Tetrode_12/phy_AGR/params.py
# 
# 
# 
# # Min L-ratio Tetrode 10 - Unit 3
# %%capture --no-display
# !phy template-gui /home/genzel/Desktop/OS_Ephys_RGS14_Rat3_357152_SD14_HC_16-11-2019_merged/cortex/Tetrode_10/phy_MS4/params.py
# 
# 
# 
# # Intermediate Values Tetrode 9 - Unit 4
# %%capture --no-display
# !phy template-gui /home/genzel/Desktop/OS_Ephys_RGS14_Rat3_357152_SD14_HC_16-11-2019_merged/cortex/Tetrode_10/phy_MS4/params.py
# 
# 
# 
# 
# 
# #%% Phy interface for high ISI violation clusters
# 
# # Tetrode 12 Unit 15
# %%capture --no-display
# !phy template-gui /home/genzel/Desktop/OS_Ephys_RGS14_Rat3_357152_SD14_HC_16-11-2019_merged/cortex/Tetrode_12/phy_AGR/params.py
# 
# 
# 
# # Tetrode 4 Unit 0
# %%capture --no-display
# !phy template-gui /home/genzel/Desktop/OS_Ephys_RGS14_Rat3_357152_SD14_HC_16-11-2019_merged/hpc/Tetrode_4/phy_AGR/params.py
# 
# 
# 
# # Tetrode 16 Unit 2
# %%capture --no-display
# !phy template-gui /home/genzel/Desktop/OS_Ephys_RGS14_Rat3_357152_SD14_HC_16-11-2019_merged/hpc/Tetrode_16/phy_AGR/params.py
# =============================================================================


























