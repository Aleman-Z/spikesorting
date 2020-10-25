#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 18:06:09 2020
SORT A TETRODE WITH .CONTINUOUS FILES (Using Manual curation)
@author: adrian
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

#Folder with tetrode data
#recording_folder='/home/adrian/Documents/SpikeSorting/Adrian_test_data/Irene_data/test_without_zero_main_channels/Tetrode_9_CH';
recording_folder=sys.argv[1];
os.chdir(recording_folder)

#Check if the recording has been preprocessed before and load it.
# Else proceed with preprocessing.
arr = os.listdir()
if 'recording.pkl' in arr:
 print('Loading previous files')
 recording_cache = se.load_extractor_from_pickle('recording.pkl')
 channel_ids = recording_cache.get_channel_ids() 
 fs = recording_cache.get_sampling_frequency()
 num_chan = recording_cache.get_num_channels()
else:
        
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
    recording_prb = recording.load_probe_file('/home/adrian/Documents/SpikeSorting/Adrian_test_data/Irene_data/test_without_zero_main_channels/Tetrode_9_CH/tetrode9.prb')
    
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
    
    #Save preprocessed data to reload at a later point.
    recording_cache.filename
    recording_cache.get_tmp_folder()
    recording_cache.move_to('preprocessed_data.dat') 
    print(recording_cache.filename)
    
    recording_cache.dump_to_dict()
    recording_cache.dump_to_pickle('recording.pkl')
    #recording_loaded = se.load_extractor_from_pickle('recording.pkl')


#View installed sorters
#ss.installed_sorters()
#mylist = [f for f in glob.glob("*.txt")]

#%% Run all channels. There are only a single tetrode channels anyway.

#Create sub recording to avoid saving whole recording.Requirement from NWB to allow saving sorters data. 
recording_sub = se.SubRecordingExtractor(recording_cache, start_frame=200*fs, end_frame=320*fs)


#Klusta
if 'sorting_KL_all.nwb' in arr:
    print('Loading Klusta')
    sorting_KL_all=se.NwbSortingExtractor('sorting_KL_all.nwb');

else:
    t = time.time()
    sorting_KL_all = ss.run_klusta(recording_cache, output_folder='results_all_klusta',delete_output_folder=True)
    print('Found', len(sorting_KL_all.get_unit_ids()), 'units')
    time.time() - t
    #Save Klusta
    se.NwbRecordingExtractor.write_recording(recording_sub, 'sorting_KL_all.nwb')
    se.NwbSortingExtractor.write_sorting(sorting_KL_all, 'sorting_KL_all.nwb')


st.postprocessing.export_to_phy(recording_cache, 
                                sorting_KL_all, output_folder='phy_manual',
                                grouping_property='group', verbose=True, recompute_info=True)


os.system('phy template-gui phy_manual/params.py') 


sorting_phy_curated = se.PhySortingExtractor('phy_manual/', exclude_cluster_groups=['noise']);


w_wf = sw.plot_unit_templates(sorting=sorting_phy_curated, recording=recording_cache)
plt.savefig('manual_unit_templates.pdf', bbox_inches='tight');
plt.savefig('manual_unit_templates.png', bbox_inches='tight');
plt.close()



sys.exit("Stop the code here")
