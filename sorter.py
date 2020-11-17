#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 16:38:09 2020

@author: adrian
"""
print('Hello World!')
import os
import sys
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

def test(folder):
    print(folder)
    os.chdir(folder)
    subfolders = [ f.name for f in os.scandir(folder) if f.is_dir() ]
    if ('phy_AGR' in subfolders):
        print('Tetrode was previously sorted. Skipping')
        return
    print(subfolders)
    


def auto(recording_folder):
    os.chdir(recording_folder)
    
    #If sorter has already been run skip it.
    subfolders = [ f.name for f in os.scandir(recording_folder) if f.is_dir() ];
    if ('phy_AGR' in subfolders):
        print('Tetrode was previously sorted. Skipping')
        return

    """
    Adding Matlab-based sorters to path
    
    """
    #IronClust
    ss.IronClustSorter.set_ironclust_path('/home/adrian/Documents/SpikeSorting/ironclust')
    ss.IronClustSorter.ironclust_path
    
    #HDSort
    ss.HDSortSorter.set_hdsort_path('/home/adrian/Documents/SpikeSorting/HDsort')
    ss.HDSortSorter.hdsort_path
    
    #Waveclus
    ss.WaveClusSorter.set_waveclus_path('/home/adrian/Documents/SpikeSorting/wave_clus')
    ss.WaveClusSorter.waveclus_path
    
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
    #recording_prb = recording.load_probe_file('/home/adrian/Documents/SpikeSorting/Adrian_test_data/Irene_data/test_without_zero_main_channels/Tetrode_9_CH/tetrode.prb')
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
        
    
    #View installed sorters
    #ss.installed_sorters()
    #mylist = [f for f in glob.glob("*.txt")]
    
    #%% Run all channels. There are only a single tetrode channels anyway.
    
    #Create sub recording to avoid saving whole recording.Requirement from NWB to allow saving sorters data. 
    recording_sub = se.SubRecordingExtractor(recording_cache, start_frame=200*fs, end_frame=320*fs)
    
    Sorters2Compare=[];
    Sorters2CompareLabel=[];
    SortersCount=[]; #Amount of detections per sorter
    
    #Klusta
    if 'sorting_KL_all.nwb' in arr:
        print('Loading Klusta')
        sorting_KL_all=se.NwbSortingExtractor('sorting_KL_all.nwb');
        if not(not(sorting_KL_all.get_unit_ids())):
            Sorters2Compare.append(sorting_KL_all);
            Sorters2CompareLabel.append('KL');
    
    else:
        t = time.time()
        sorting_KL_all = ss.run_klusta(recording_cache, output_folder='results_all_klusta',delete_output_folder=True)
        print('Found', len(sorting_KL_all.get_unit_ids()), 'units')
        time.time() - t
        #Save Klusta
        se.NwbRecordingExtractor.write_recording(recording_sub, 'sorting_KL_all.nwb')
        se.NwbSortingExtractor.write_sorting(sorting_KL_all, 'sorting_KL_all.nwb')
        if not(not(sorting_KL_all.get_unit_ids())):
            Sorters2Compare.append(sorting_KL_all);
            Sorters2CompareLabel.append('KL');
    SortersCount.append(len(sorting_KL_all.get_unit_ids()))
    
    #Ironclust
    if 'sorting_IC_all.nwb' in arr:
        print('Loading Ironclust')
        sorting_IC_all=se.NwbSortingExtractor('sorting_IC_all.nwb');     
        if not(not(sorting_IC_all.get_unit_ids())):
            Sorters2Compare.append(sorting_IC_all);
            Sorters2CompareLabel.append('IC');
    
    else:
        t = time.time()
        sorting_IC_all = ss.run_ironclust(recording_cache, output_folder='results_all_ic',delete_output_folder=True)
        print('Found', len(sorting_IC_all.get_unit_ids()), 'units')
        time.time() - t
        #Save IC
        se.NwbRecordingExtractor.write_recording(recording_sub, 'sorting_IC_all.nwb')
        se.NwbSortingExtractor.write_sorting(sorting_IC_all, 'sorting_IC_all.nwb')
        if not(not(sorting_IC_all.get_unit_ids())):
            Sorters2Compare.append(sorting_IC_all);
            Sorters2CompareLabel.append('IC');
    SortersCount.append(len(sorting_IC_all.get_unit_ids()))
        
    #Waveclust
    if 'sorting_waveclus_all.nwb' in arr:
        print('Loading waveclus')
        sorting_waveclus_all=se.NwbSortingExtractor('sorting_waveclus_all.nwb');
        if not(not(sorting_waveclus_all.get_unit_ids())):
            Sorters2Compare.append(sorting_waveclus_all);
            Sorters2CompareLabel.append('Waveclus');
        
    else:
        t = time.time()
        sorting_waveclus_all = ss.run_waveclus(recording_cache, output_folder='results_all_waveclus',delete_output_folder=True)
        print('Found', len(sorting_waveclus_all.get_unit_ids()), 'units')
        time.time() - t
        #Save waveclus
        se.NwbRecordingExtractor.write_recording(recording_sub, 'sorting_waveclus_all.nwb')
        se.NwbSortingExtractor.write_sorting(sorting_waveclus_all, 'sorting_waveclus_all.nwb')
        if not(not(sorting_waveclus_all.get_unit_ids())):
            Sorters2Compare.append(sorting_waveclus_all);
            Sorters2CompareLabel.append('Waveclus');
    SortersCount.append(len(sorting_waveclus_all.get_unit_ids()))
    
    #Herdingspikes
    if 'sorting_herdingspikes_all.nwb' in arr:
        print('Loading herdingspikes')
        sorting_herdingspikes_all=se.NwbSortingExtractor('sorting_heardingspikes_all.nwb');
        if not(not(sorting_herdingspikes_all.get_unit_ids())):
            Sorters2Compare.append(sorting_herdingspikes_all);
            Sorters2CompareLabel.append('HS');
    
    else:
        t = time.time()
        #When herdingspikes fails, assign the results from Klusta.
        try:
            sorting_herdingspikes_all = ss.run_herdingspikes(recording_cache, output_folder='results_all_herdingspikes',delete_output_folder=True)
        except:
            print('Herdingspikes has failed')
            sorting_herdingspikes_all =sorting_KL_all;
        print('Found', len(sorting_herdingspikes_all.get_unit_ids()), 'units')
        time.time() - t
        #Save herdingspikes
        se.NwbRecordingExtractor.write_recording(recording_cache, 'sorting_herdingspikes_all.nwb')
        try: 
            se.NwbSortingExtractor.write_sorting(sorting_herdingspikes_all, 'sorting_herdingspikes_all.nwb')
        except TypeError:
            print("No units detected.  Can't save HerdingSpikes")
            os.remove("sorting_herdingspikes_all.nwb")
        if not(not(sorting_herdingspikes_all.get_unit_ids())):
            Sorters2Compare.append(sorting_herdingspikes_all);
            Sorters2CompareLabel.append('HS');
    SortersCount.append(len(sorting_herdingspikes_all.get_unit_ids()))    
    
    #Mountainsort4
    if 'sorting_mountainsort4_all.nwb' in arr:
        print('Loading mountainsort4')
        sorting_mountainsort4_all=se.NwbSortingExtractor('sorting_mountainsort4_all.nwb');
        if not(not(sorting_mountainsort4_all.get_unit_ids())):
            Sorters2Compare.append(sorting_mountainsort4_all);
            Sorters2CompareLabel.append('MS4');
    
    else:
        t = time.time()
        sorting_mountainsort4_all = ss.run_mountainsort4(recording_cache, output_folder='results_all_mountainsort4',delete_output_folder=True)
        print('Found', len(sorting_mountainsort4_all.get_unit_ids()), 'units')
        time.time() - t
        #Save mountainsort4
        se.NwbRecordingExtractor.write_recording(recording_sub, 'sorting_mountainsort4_all.nwb')
        se.NwbSortingExtractor.write_sorting(sorting_mountainsort4_all, 'sorting_mountainsort4_all.nwb')
        if not(not(sorting_mountainsort4_all.get_unit_ids())):
            Sorters2Compare.append(sorting_mountainsort4_all);
            Sorters2CompareLabel.append('MS4');
    SortersCount.append(len(sorting_mountainsort4_all.get_unit_ids()))    
    
        
    #Spykingcircus
    if 'sorting_spykingcircus_all.nwb' in arr:
        print('Loading spykingcircus')
        sorting_spykingcircus_all=se.NwbSortingExtractor('sorting_spykingcircus_all.nwb');
        if not(not(sorting_spykingcircus_all.get_unit_ids())):
            Sorters2Compare.append(sorting_spykingcircus_all);
            Sorters2CompareLabel.append('SC');
    
    else:
        t = time.time()
        sorting_spykingcircus_all = ss.run_spykingcircus(recording_cache, output_folder='results_all_spykingcircus',delete_output_folder=True)
        print('Found', len(sorting_spykingcircus_all.get_unit_ids()), 'units')
        time.time() - t
        #Save sorting_spykingcircus
        se.NwbRecordingExtractor.write_recording(recording_sub, 'sorting_spykingcircus_all.nwb')
        se.NwbSortingExtractor.write_sorting(sorting_spykingcircus_all, 'sorting_spykingcircus_all.nwb')
        if not(not(sorting_spykingcircus_all.get_unit_ids())):
            Sorters2Compare.append(sorting_spykingcircus_all);
            Sorters2CompareLabel.append('SC');
    SortersCount.append(len(sorting_spykingcircus_all.get_unit_ids()))    
    
        
    #Tridesclous
    if 'sorting_tridesclous_all.nwb' in arr:
        print('Loading tridesclous')
        try:
            sorting_tridesclous_all=se.NwbSortingExtractor('sorting_tridesclous_all.nwb');
        except AttributeError:
            print("No units detected.  Can't load Tridesclous so will run it.")
            t = time.time()
            sorting_tridesclous_all = ss.run_tridesclous(recording_cache, output_folder='results_all_tridesclous',delete_output_folder=True)
            print('Found', len(sorting_tridesclous_all.get_unit_ids()), 'units')
            time.time() - t
            os.remove("sorting_tridesclous_all.nwb") 
            #Save sorting_tridesclous
            se.NwbRecordingExtractor.write_recording(recording_sub, 'sorting_tridesclous_all.nwb')
            se.NwbSortingExtractor.write_sorting(sorting_tridesclous_all, 'sorting_tridesclous_all.nwb') 
        if not(not(sorting_tridesclous_all.get_unit_ids())):
            Sorters2Compare.append(sorting_tridesclous_all);
            Sorters2CompareLabel.append('TRI');
                  
    else:
        t = time.time()
        sorting_tridesclous_all = ss.run_tridesclous(recording_cache, output_folder='results_all_tridesclous',delete_output_folder=True)
        print('Found', len(sorting_tridesclous_all.get_unit_ids()), 'units')
        time.time() - t
        #Save sorting_tridesclous
        se.NwbRecordingExtractor.write_recording(recording_sub, 'sorting_tridesclous_all.nwb')
        se.NwbSortingExtractor.write_sorting(sorting_tridesclous_all, 'sorting_tridesclous_all.nwb')
        if not(not(sorting_tridesclous_all.get_unit_ids())):
            Sorters2Compare.append(sorting_tridesclous_all);
            Sorters2CompareLabel.append('TRI');
    SortersCount.append(len(sorting_tridesclous_all.get_unit_ids()))    
    
    
    #Consensus based curation.
    print(Sorters2CompareLabel)
    print('Comparing sorters agreement. Please wait...')
    mcmp = sc.compare_multiple_sorters(Sorters2Compare, Sorters2CompareLabel)
    w = sw.plot_multicomp_agreement_by_sorter(mcmp)
    # plt.show()
    plt.savefig('consensus.pdf', bbox_inches='tight');
    plt.savefig('consensus.png', bbox_inches='tight');
    plt.close()
    
    w = sw.plot_multicomp_agreement(mcmp)
    plt.savefig('consensus_spikes.pdf', bbox_inches='tight');
    plt.savefig('consensus_spikes.png', bbox_inches='tight');
    plt.close()
    
    
    #Use amount of sorters which give a value closest to 10 units.
    agreed_units=[];
    for x in [1,2,3,4,5]:
        agreement_sorting = mcmp.get_agreement_sorting(minimum_agreement_count=x)
        agreed_units.append(len(agreement_sorting.get_unit_ids()));
    print(agreed_units)
    print(agreed_units.index(min(agreed_units, key=lambda x:abs(x-10)))+1)
    
    agreement_sorting = mcmp.get_agreement_sorting(minimum_agreement_count=
            agreed_units.index(min(agreed_units, key=lambda x:abs(x-10)))+1);
    
    print(agreement_sorting.get_unit_ids())
    if not(agreement_sorting.get_unit_ids()): #If there is no agreement.
        print('No consensus. Finding sorter with closest to expected amount of units')
        print(Sorters2CompareLabel[SortersCount.index(min(SortersCount, key=lambda x:abs(x-10)))])
        agreement_sorting=Sorters2Compare[SortersCount.index(min(SortersCount, key=lambda x:abs(x-10)))]
       
    st.postprocessing.export_to_phy(recording_cache, 
                                    agreement_sorting, output_folder='phy_AGR',
                                    grouping_property='group', verbose=True, recompute_info=True)
    
    
    # se.NwbRecordingExtractor.write_recording(recording_sub, 'agreement_sorting.nwb')
    # se.NwbSortingExtractor.write_sorting(agreement_sorting, 'agreement_sorting.nwb')
    
    # os.system('phy template-gui phy_AGR/params.py') 
    # sorting_phy_curated = se.PhySortingExtractor('phy_AGR/', exclude_cluster_groups=['noise']);
    
    
    # se.NwbRecordingExtractor.write_recording(recording_sub, 'consensus_phy_curated.nwb')
    # se.NwbSortingExtractor.write_sorting(sorting_phy_curated, 'consensus_phy_curated.nwb') 
    
    
    w_wf = sw.plot_unit_templates(sorting=agreement_sorting, recording=recording_cache)
    plt.savefig('unit_templates.pdf', bbox_inches='tight');
    plt.savefig('unit_templates.png', bbox_inches='tight');
    plt.close()
    
    
    #Access unit ID and firing rate.
    os.chdir('phy_AGR')
    spike_times=np.load('spike_times.npy');
    spike_clusters=np.load('spike_clusters.npy');
    
    #Create a list with the unit IDs
    some_list=np.unique(spike_clusters)
    some_list=some_list.tolist()
    
    #Bin data in bins of 25ms
    #45 minutes
    bins=np.arange(start=0, stop=45*60*fs+1, step=.025*fs)
    NData=np.zeros([np.unique(spike_clusters).shape[0],bins.shape[0]-1])
    
    cont=0;
    for x in some_list:
        ind=(spike_clusters==x)
        fi=spike_times[ind]
        inds = np.histogram(fi, bins=bins)
        inds1=inds[0]
        NData[cont,:]=inds1;
        cont=cont+1;
    
    #Save activation matrix
    os.chdir("..")
    a=os.path.split(os.getcwd())[1]
    np.save('actmat_auto_'+a.split('_')[1], NData)
    np.save('unit_id_auto_'+a.split('_')[1],some_list)
    

def manual(recording_folder):
    #Folder with tetrode data
    #recording_folder='/home/adrian/Documents/SpikeSorting/Adrian_test_data/Irene_data/test_without_zero_main_channels/Tetrode_9_CH';
    
    os.chdir(recording_folder)
    
    #If sorter has already been run skip it.
    subfolders = [ f.name for f in os.scandir(recording_folder) if f.is_dir() ];
    if ('phy_manual' in subfolders):
        print('Tetrode was previously manually sorted. Skipping')
        return

    
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
    
    

if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])