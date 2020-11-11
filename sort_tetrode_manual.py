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
import csv

#Folder with tetrode data
#recording_folder='/home/adrian/Documents/SpikeSorting/Adrian_test_data/Irene_data/test_without_zero_main_channels/Tetrode_9_CH';
recording_folder=sys.argv[1];
os.chdir(recording_folder)

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
recording_prb = recording.load_probe_file(os.getcwd()+'/tetrode.prb')

print('Channels after loading the probe file:', recording_prb.get_channel_ids())
print('Channel groups after loading the probe file:', recording_prb.get_channel_groups())

#For testing only: Reduce recording.
#recording_prb = se.SubRecordingExtractor(recording_prb, start_frame=100*fs, end_frame=420*fs)


#Bandpass filter 
recording_cmr = st.preprocessing.bandpass_filter(recording_prb, freq_min=300, freq_max=6000)
recording_cache = se.CacheRecordingExtractor(recording_cmr);


print(recording_cache.get_channel_ids())
print(recording_cache.get_channel_groups())
print(recording_cache.get_num_frames() / recording_cache.get_sampling_frequency())

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
    print(time.time() - t)
    #Save Klusta
    se.NwbRecordingExtractor.write_recording(recording_sub, 'sorting_KL_all.nwb')
    se.NwbSortingExtractor.write_sorting(sorting_KL_all, 'sorting_KL_all.nwb')


st.postprocessing.export_to_phy(recording_cache, 
                                sorting_KL_all, output_folder='phy_manual',
                                grouping_property='group', verbose=True, recompute_info=True)

#Open phy interface
os.system('phy template-gui phy_manual/params.py') 

#Remove detections curated as noise.
sorting_phy_curated = se.PhySortingExtractor('phy_manual/', exclude_cluster_groups=['noise']);

#Print waveforms of units
w_wf = sw.plot_unit_templates(sorting=sorting_phy_curated, recording=recording_cache)
plt.savefig('manual_unit_templates.pdf', bbox_inches='tight');
plt.savefig('manual_unit_templates.png', bbox_inches='tight');
plt.close()

#Access unit ID and firing rate.
os.chdir('phy_manual')
spike_times=np.load('spike_times.npy');
spike_clusters=np.load('spike_clusters.npy');
#Find units curated as 'noise'
noise_id=[];    
with open("cluster_group.tsv") as fd:
    rd = csv.reader(fd, delimiter="\t", quotechar='"')
    for row in rd:
        if row[1]=='noise':
            noise_id.append(int(row[0]))
#Create a list with the unit IDs and remove those labeled as 'noise'
some_list=np.unique(spike_clusters)
some_list=some_list.tolist()
for x in noise_id:    
    print(x)
    some_list.remove(x)

#Bin data in bins of 25ms
#45 minutes
bins=np.arange(start=0, stop=45*60*fs+1, step=.025*fs)
NData=np.zeros([np.unique(spike_clusters).shape[0]-len(noise_id),bins.shape[0]-1])

cont=0;    
for x in some_list:    
    #print(x)
    ind=(spike_clusters==x)
    fi=spike_times[ind]
    inds = np.histogram(fi, bins=bins)
    inds1=inds[0]
    NData[cont,:]=inds1;
    cont=cont+1;


#Save activation matrix
os.chdir("..")
a=os.path.split(os.getcwd())[1]
np.save('actmat_manual_'+a.split('_')[1], NData)
np.save('unit_id_manual_'+a.split('_')[1],some_list)

sys.exit("Stop the code here")
