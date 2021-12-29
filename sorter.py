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
from shutil import rmtree
    
def auto(recording_folder):
    os.chdir(recording_folder)
    
    #If sorter has already been run skip it.
    subfolders = [ f.name for f in os.scandir(recording_folder) if f.is_dir() ];
    if ('phy_AGR' in subfolders) or ('phy_MS4' in subfolders):
        print('Tetrode '+recording_folder.split('_')[-1]+' was previously sorted. Skipping')
        return

    """
    Adding Matlab-based sorters to path
    
    """
        
    #IronClust
    iron_path = "~/Documents/SpikeSorting/ironclust";    
    ss.IronClustSorter.set_ironclust_path(os.path.expanduser(iron_path))
    ss.IronClustSorter.ironclust_path
    
    #HDSort
    #ss.HDSortSorter.set_hdsort_path('/home/adrian/Documents/SpikeSorting/HDsort')
    #ss.HDSortSorter.hdsort_path
    
    #Waveclus
    #ss.WaveClusSorter.set_waveclus_path('/home/adrian/Documents/SpikeSorting/wave_clus')
    #ss.WaveClusSorter.waveclus_path
    
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
        SortersCount.append(len(sorting_IC_all.get_unit_ids()))
    
    else:
        try:
            t = time.time()
            sorting_IC_all = ss.run_ironclust(recording_cache, output_folder='results_all_ic',delete_output_folder=True, filter=False)
            print('Found', len(sorting_IC_all.get_unit_ids()), 'units')
            time.time() - t
            #Save IC
            se.NwbRecordingExtractor.write_recording(recording_sub, 'sorting_IC_all.nwb')
            se.NwbSortingExtractor.write_sorting(sorting_IC_all, 'sorting_IC_all.nwb')
            if not(not(sorting_IC_all.get_unit_ids())):
                Sorters2Compare.append(sorting_IC_all);
                Sorters2CompareLabel.append('IC');
            SortersCount.append(len(sorting_IC_all.get_unit_ids()))
        except:       
            print('Ironclust has failed')

    # #Waveclust
    # if 'sorting_waveclus_all.nwb' in arr:
    #     print('Loading waveclus')
    #     sorting_waveclus_all=se.NwbSortingExtractor('sorting_waveclus_all.nwb');
    #     if not(not(sorting_waveclus_all.get_unit_ids())):
    #         Sorters2Compare.append(sorting_waveclus_all);
    #         Sorters2CompareLabel.append('Waveclus');
    #     SortersCount.append(len(sorting_waveclus_all.get_unit_ids()))    
        
    # else:
    #     t = time.time()
    #     try:
    #         sorting_waveclus_all = ss.run_waveclus(recording_cache, output_folder='results_all_waveclus',delete_output_folder=True)
    #         print('Found', len(sorting_waveclus_all.get_unit_ids()), 'units')
    #         time.time() - t
    #         #Save waveclus
    #         se.NwbRecordingExtractor.write_recording(recording_sub, 'sorting_waveclus_all.nwb')
    #         se.NwbSortingExtractor.write_sorting(sorting_waveclus_all, 'sorting_waveclus_all.nwb')
    #         if not(not(sorting_waveclus_all.get_unit_ids())):
    #             Sorters2Compare.append(sorting_waveclus_all);
    #             Sorters2CompareLabel.append('Waveclus');
    #         SortersCount.append(len(sorting_waveclus_all.get_unit_ids()))
    #     except:
    #         print('Waveclus cannot be run')
    
    #Herdingspikes
    if 'sorting_herdingspikes_all.nwb' in arr:
        print('Loading herdingspikes')
        sorting_herdingspikes_all=se.NwbSortingExtractor('sorting_herdingspikes_all.nwb');
        if not(not(sorting_herdingspikes_all.get_unit_ids())):
            Sorters2Compare.append(sorting_herdingspikes_all);
            Sorters2CompareLabel.append('HS');
        SortersCount.append(len(sorting_herdingspikes_all.get_unit_ids()))        
    
    else:
        try:
            t = time.time()
            sorting_herdingspikes_all = ss.run_herdingspikes(recording_cache, output_folder='results_all_herdingspikes',delete_output_folder=True)
    
            print('Found', len(sorting_herdingspikes_all.get_unit_ids()), 'units')
            time.time() - t
            #Save herdingspikes
            se.NwbRecordingExtractor.write_recording(recording_sub, 'sorting_herdingspikes_all.nwb')
            try: 
                se.NwbSortingExtractor.write_sorting(sorting_herdingspikes_all, 'sorting_herdingspikes_all.nwb')
            except TypeError:
                print("No units detected.  Can't save HerdingSpikes")
                os.remove("sorting_herdingspikes_all.nwb")
            if not(not(sorting_herdingspikes_all.get_unit_ids())):
                Sorters2Compare.append(sorting_herdingspikes_all);
                Sorters2CompareLabel.append('HS');
            SortersCount.append(len(sorting_herdingspikes_all.get_unit_ids()))    
            
        except:
                print('Herdingspikes has failed')
                
    try:
        rmtree("results_all_herdingspikes")
    except:
        print('Removed leftover herdingspikes files')
        
    try:
        rmtree("results_all_herdingspikes")
    except:
        print('Removed leftover herdingspikes files')
        
    #Mountainsort4
    if 'sorting_mountainsort4_all.nwb' in arr:
        print('Loading mountainsort4')
        sorting_mountainsort4_all=se.NwbSortingExtractor('sorting_mountainsort4_all.nwb');
        if not(not(sorting_mountainsort4_all.get_unit_ids())):
            Sorters2Compare.append(sorting_mountainsort4_all);
            Sorters2CompareLabel.append('MS4');
    
    else:
        t = time.time()
        sorting_mountainsort4_all = ss.run_mountainsort4(recording_cache, output_folder='results_all_mountainsort4',delete_output_folder=True, filter=False)
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
        SortersCount.append(len(sorting_spykingcircus_all.get_unit_ids()))    
    
    else:
        try:
            t = time.time()
            sorting_spykingcircus_all = ss.run_spykingcircus(recording_cache, output_folder='results_all_spykingcircus',delete_output_folder=True, filter=False)
            print('Found', len(sorting_spykingcircus_all.get_unit_ids()), 'units')
            time.time() - t
            #Save sorting_spykingcircus
            se.NwbRecordingExtractor.write_recording(recording_sub, 'sorting_spykingcircus_all.nwb')
            se.NwbSortingExtractor.write_sorting(sorting_spykingcircus_all, 'sorting_spykingcircus_all.nwb')
            if not(not(sorting_spykingcircus_all.get_unit_ids())):
                Sorters2Compare.append(sorting_spykingcircus_all);
                Sorters2CompareLabel.append('SC');
            SortersCount.append(len(sorting_spykingcircus_all.get_unit_ids()))    
        except:
                print('Spykingcircus has failed')
                
        
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
        SortersCount.append(len(sorting_tridesclous_all.get_unit_ids()))    
                      
    else:
        try:
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
    
        except:
                print('Tridesclous failed')
                
                   
    try:
        rmtree("results_all_tridesclous")
    except:
        print('Removed leftover tridesclous files')
    
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
    
    
    # #Use amount of sorters which give a value closest to 10 units.
    # agreed_units=[];
    # for x in [1,2,3,4,5]:
    #     agreement_sorting = mcmp.get_agreement_sorting(minimum_agreement_count=x)
    #     agreed_units.append(len(agreement_sorting.get_unit_ids()));
    # print(agreed_units)
    # print(agreed_units.index(min(agreed_units, key=lambda x:abs(x-10)))+1)
    
    # agreement_sorting = mcmp.get_agreement_sorting(minimum_agreement_count=
    #         agreed_units.index(min(agreed_units, key=lambda x:abs(x-10)))+1);
    
    # Use units with at least 2 sorters agreeing.
    agreement_sorting = mcmp.get_agreement_sorting(minimum_agreement_count=2)
    
    print(agreement_sorting.get_unit_ids())
    phy_folder_name='phy_AGR';
    if not(agreement_sorting.get_unit_ids()): #If there is no agreement.
        # print('No consensus. Finding sorter with closest to expected amount of units')
        # print(Sorters2CompareLabel[SortersCount.index(min(SortersCount, key=lambda x:abs(x-10)))])
        # agreement_sorting=Sorters2Compare[SortersCount.index(min(SortersCount, key=lambda x:abs(x-10)))]
        print('No consensus. Using detections from MountainSort4')
        agreement_sorting=sorting_mountainsort4_all;
        phy_folder_name='phy_MS4';
        
    st.postprocessing.export_to_phy(recording_cache, 
                                    agreement_sorting, output_folder=phy_folder_name,
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
    os.chdir(phy_folder_name)
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
    #exit()

def manual(recording_folder):
    #Folder with tetrode data
    #recording_folder='/home/adrian/Documents/SpikeSorting/Adrian_test_data/Irene_data/test_without_zero_main_channels/Tetrode_9_CH';
    
    os.chdir(recording_folder)
    
    """
    Adding Matlab-based sorters to path
    
    """
        
    #IronClust
    iron_path = "~/Documents/SpikeSorting/ironclust";    
    ss.IronClustSorter.set_ironclust_path(os.path.expanduser(iron_path))
    ss.IronClustSorter.ironclust_path
    
    #If sorter has already been run skip it.
    subfolders = [ f.name for f in os.scandir(recording_folder) if f.is_dir() ];
    #if ('phy_KL' in subfolders) & ('phy_IC' in subfolders) & ('phy_Waveclus' in subfolders) & ('phy_SC' in subfolders) & ('phy_MS4' in subfolders) & ('phy_HS' in subfolders) & ('phy_TRI' in subfolders):
    if ('phy_KL' in subfolders) & ('phy_IC' in subfolders) & ('phy_SC' in subfolders) & ('phy_MS4' in subfolders) & ('phy_HS' in subfolders) & ('phy_TRI' in subfolders):
        print('Tetrode '+recording_folder.split('_')[-1]+' was previously manually sorted. Skipping')
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
    
    #%% Run all channels. There are only single tetrode channels anyway.
    
    #Create sub recording to avoid saving whole recording.Requirement from NWB to allow saving sorters data. 
    recording_sub = se.SubRecordingExtractor(recording_cache, start_frame=200*fs, end_frame=320*fs)
    # Sorters2CompareLabel=['KL','IC','Waveclus','HS','MS4','SC','TRI'];
    Sorters2CompareLabel=['KL','IC','HS','MS4','SC','TRI'];
    subfolders = [ f.name for f in os.scandir(recording_folder) if f.is_dir() ];
    
    for num in range(len(Sorters2CompareLabel)):
    
        i=Sorters2CompareLabel[num];
        print(i) 
        if 'phy_'+i in subfolders:
            print('Sorter already used for curation. Skipping')
            continue
        else:
        
            if 'KL' in i:
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
                sorter=sorting_KL_all;
            
            if 'IC' in i:
                #Ironclust
                if 'sorting_IC_all.nwb' in arr:
                    print('Loading Ironclust')
                    sorting_IC_all=se.NwbSortingExtractor('sorting_IC_all.nwb');     
                
                else:
                    t = time.time()
                    sorting_IC_all = ss.run_ironclust(recording_cache, output_folder='results_all_ic',delete_output_folder=True, filter=False)
                    print('Found', len(sorting_IC_all.get_unit_ids()), 'units')
                    print(time.time() - t)
                    #Save IC
                    se.NwbRecordingExtractor.write_recording(recording_sub, 'sorting_IC_all.nwb')
                    se.NwbSortingExtractor.write_sorting(sorting_IC_all, 'sorting_IC_all.nwb')
                sorter=sorting_IC_all;
            
            # if 'Waveclus' in i:
            #     #Waveclust
            #     if 'sorting_waveclus_all.nwb' in arr:
            #         print('Loading waveclus')
            #         sorting_waveclus_all=se.NwbSortingExtractor('sorting_waveclus_all.nwb');
                    
            #     else:
            #         t = time.time()
            #         sorting_waveclus_all = ss.run_waveclus(recording_cache, output_folder='results_all_waveclus',delete_output_folder=True)
            #         print('Found', len(sorting_waveclus_all.get_unit_ids()), 'units')
            #         print(time.time() - t)
            #         #Save waveclus
            #         se.NwbRecordingExtractor.write_recording(recording_sub, 'sorting_waveclus_all.nwb')
            #         se.NwbSortingExtractor.write_sorting(sorting_waveclus_all, 'sorting_waveclus_all.nwb')
            #     sorter=sorting_waveclus_all;
            
            if 'HS' in i:
                #Herdingspikes
                if 'sorting_herdingspikes_all.nwb' in arr:
                    print('Loading herdingspikes')
                    sorting_herdingspikes_all=se.NwbSortingExtractor('sorting_herdingspikes_all.nwb');
                    sorter=sorting_herdingspikes_all;
                
                else:
                    t = time.time()
                    try:
                        sorting_herdingspikes_all = ss.run_herdingspikes(recording_cache, output_folder='results_all_herdingspikes',delete_output_folder=True)
                        print('Found', len(sorting_herdingspikes_all.get_unit_ids()), 'units')
                        time.time() - t
                        #Save herdingspikes
                        se.NwbRecordingExtractor.write_recording(recording_sub, 'sorting_herdingspikes_all.nwb')
                        try: 
                            se.NwbSortingExtractor.write_sorting(sorting_herdingspikes_all, 'sorting_herdingspikes_all.nwb')
                        except TypeError:
                            print("No units detected.  Can't save HerdingSpikes")
                            os.remove("sorting_herdingspikes_all.nwb")
                        sorter=sorting_herdingspikes_all;                        
                    except:
                            print('Herdingspikes has failed')
                            sorter=[];
            
            if 'MS4' in i:
                #Mountainsort4
                if 'sorting_mountainsort4_all.nwb' in arr:
                    print('Loading mountainsort4')
                    sorting_mountainsort4_all=se.NwbSortingExtractor('sorting_mountainsort4_all.nwb');
                
                else:
                    t = time.time()
                    sorting_mountainsort4_all = ss.run_mountainsort4(recording_cache, output_folder='results_all_mountainsort4',delete_output_folder=True, filter=False)
                    print('Found', len(sorting_mountainsort4_all.get_unit_ids()), 'units')
                    print(time.time() - t)
                    #Save mountainsort4
                    se.NwbRecordingExtractor.write_recording(recording_sub, 'sorting_mountainsort4_all.nwb')
                    se.NwbSortingExtractor.write_sorting(sorting_mountainsort4_all, 'sorting_mountainsort4_all.nwb')
                sorter=sorting_mountainsort4_all;
            
            if 'SC' in i:
                #Spykingcircus
                if 'sorting_spykingcircus_all.nwb' in arr:
                    print('Loading spykingcircus')
                    sorting_spykingcircus_all=se.NwbSortingExtractor('sorting_spykingcircus_all.nwb', filter=False);
                
                else:
                    t = time.time()
                    sorting_spykingcircus_all = ss.run_spykingcircus(recording_cache, output_folder='results_all_spykingcircus',delete_output_folder=True)
                    print('Found', len(sorting_spykingcircus_all.get_unit_ids()), 'units')
                    print(time.time() - t)
                    #Save sorting_spykingcircus
                    se.NwbRecordingExtractor.write_recording(recording_sub, 'sorting_spykingcircus_all.nwb')
                    se.NwbSortingExtractor.write_sorting(sorting_spykingcircus_all, 'sorting_spykingcircus_all.nwb')
                sorter=sorting_spykingcircus_all;
            
            if 'TRI' in i:
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
                              
                else:
                    t = time.time()
                    sorting_tridesclous_all = ss.run_tridesclous(recording_cache, output_folder='results_all_tridesclous',delete_output_folder=True)
                    print('Found', len(sorting_tridesclous_all.get_unit_ids()), 'units')
                    time.time() - t
                    #Save sorting_tridesclous
                    se.NwbRecordingExtractor.write_recording(recording_sub, 'sorting_tridesclous_all.nwb')
                    se.NwbSortingExtractor.write_sorting(sorting_tridesclous_all, 'sorting_tridesclous_all.nwb')
                sorter=sorting_tridesclous_all;
            
           #Check if sorter failed  
            if not sorter:
                continue                
            
            st.postprocessing.export_to_phy(recording_cache, 
                                            sorter, output_folder='phy_'+i,
                                            grouping_property='group', verbose=True, recompute_info=True)
            
            #Open phy interface
            os.system('phy template-gui phy_'+i+'/params.py') 
           
                
            #Remove detections curated as noise.
            sorting_phy_curated = se.PhySortingExtractor('phy_'+i+'/', exclude_cluster_groups=['noise']);
            
            #Print waveforms of units
            w_wf = sw.plot_unit_templates(sorting=sorting_phy_curated, recording=recording_cache)
            plt.savefig('manual_'+i+'_unit_templates.pdf', bbox_inches='tight');
            plt.savefig('manual_'+i+'_unit_templates.png', bbox_inches='tight');
            plt.close()
            
            #Compute agreement matrix wrt consensus-based sorting.
            sorting_phy_consensus = se.PhySortingExtractor('phy_AGR/', exclude_cluster_groups=['noise']);
            cmp=sc.compare_sorter_to_ground_truth(sorting_phy_curated,sorting_phy_consensus)
            sw.plot_agreement_matrix(cmp)
            plt.savefig('agreement_matrix_'+i+'.pdf', bbox_inches='tight');
            plt.savefig('agreement_matrix_'+i+'.png', bbox_inches='tight');
            plt.close()
            
            
            #Access unit ID and firing rate.
            os.chdir('phy_'+i)
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
            np.save('actmat_manual_'+i+'_'+a.split('_')[1], NData)
            np.save('unit_id_manual_'+i+'_'+a.split('_')[1],some_list)
    
    #End of for loop
    print("Stop the code here")
    
def ms4(recording_folder):
    
    os.chdir(recording_folder)
    
    #If sorter has already been run skip it.
    subfolders = [ f.name for f in os.scandir(recording_folder) if f.is_dir() ];
    if ('phy_MS4' in subfolders):
        print('Tetrode '+recording_folder.split('_')[-1]+' was previously sorted. Skipping')
        return
    
    print('Running Mountain Sort 4 on Tetrode '+recording_folder.split('_')[-1])

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
        
    
    #%% Run all channels. There are only a single tetrode channels anyway.
    
    #Create sub recording to avoid saving whole recording.Requirement from NWB to allow saving sorters data. 
    recording_sub = se.SubRecordingExtractor(recording_cache, start_frame=200*fs, end_frame=320*fs)
        
    #Mountainsort4
    if 'sorting_mountainsort4_all.nwb' in arr:
        print('Loading mountainsort4')
        sorting_mountainsort4_all=se.NwbSortingExtractor('sorting_mountainsort4_all.nwb');
    
    else:
        t = time.time()
        sorting_mountainsort4_all = ss.run_mountainsort4(recording_cache, output_folder='results_all_mountainsort4',delete_output_folder=True, filter=False)
        print('Found', len(sorting_mountainsort4_all.get_unit_ids()), 'units')
        time.time() - t
        #Save mountainsort4
        se.NwbRecordingExtractor.write_recording(recording_sub, 'sorting_mountainsort4_all.nwb')
        se.NwbSortingExtractor.write_sorting(sorting_mountainsort4_all, 'sorting_mountainsort4_all.nwb')
    
        
    
    

    
    print(sorting_mountainsort4_all.get_unit_ids())
        
    st.postprocessing.export_to_phy(recording_cache, 
                                    sorting_mountainsort4_all, output_folder='phy_MS4',
                                    grouping_property='group', verbose=True, recompute_info=True)
            
    w_wf = sw.plot_unit_templates(sorting=sorting_mountainsort4_all, recording=recording_cache)
    plt.savefig('unit_templates.pdf', bbox_inches='tight');
    plt.savefig('unit_templates.png', bbox_inches='tight');
    plt.close()
    
    
    #Access unit ID and firing rate.
    os.chdir('phy_MS4')
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
    #exit()
    
def manual_phy(recording_folder):
    os.chdir(recording_folder)
    
    arr = os.listdir()
    
    a=os.path.split(os.getcwd())[1]
    actmat_file=('actmat_manual_'+a.split('_')[1]);

    #If sorter has already been run skip it.
    if (actmat_file+'.npy' in arr):
        print('Tetrode '+recording_folder.split('_')[-1]+' was previously manually sorted. Skipping')
        return

    
    
    subfolders = [ f.name for f in os.scandir(recording_folder) if f.is_dir() ];
    phy_folder = [s for s in subfolders if "phy" in s]
    
        
    # #Load .continuous files 
    # recording = se.OpenEphysRecordingExtractor(recording_folder) 
    # channel_ids = recording.get_channel_ids() 
    # fs = recording.get_sampling_frequency()
    # num_chan = recording.get_num_channels()
    
    
    # print('Channel ids:', channel_ids)
    # print('Sampling frequency:', fs)
    # print('Number of channels:', num_chan)
    
    
    # #!cat tetrode9.prb #Asks for prb file
    # # os.system('cat /home/adrian/Documents/SpikeSorting/Adrian_test_data/Irene_data/test_without_zero_main_channels/Tetrode_9_CH/tetrode9.prb') 
    # recording_prb = recording.load_probe_file(os.getcwd()+'/tetrode.prb')
    
    # print('Channels after loading the probe file:', recording_prb.get_channel_ids())
    # print('Channel groups after loading the probe file:', recording_prb.get_channel_groups())
    
    # #For testing only: Reduce recording.
    # #recording_prb = se.SubRecordingExtractor(recording_prb, start_frame=100*fs, end_frame=420*fs)
    
    
    # #Bandpass filter 
    # recording_cmr = st.preprocessing.bandpass_filter(recording_prb, freq_min=300, freq_max=6000)
    # recording_cache = se.CacheRecordingExtractor(recording_cmr);
    
    
    # print(recording_cache.get_channel_ids())
    # print(recording_cache.get_channel_groups())
    # print(recording_cache.get_num_frames() / recording_cache.get_sampling_frequency())
    
      
    #Open phy interface
    os.system('phy template-gui '+phy_folder[0]+'/params.py') 
   
    
    #Print waveforms of units
    # w_wf = sw.plot_unit_templates(sorting=sorting_phy_curated, recording=recording_cache)
    # plt.savefig('manual_'+i+'_unit_templates.pdf', bbox_inches='tight');
    # plt.savefig('manual_'+i+'_unit_templates.png', bbox_inches='tight');
    # plt.close()
    
        
    #Access unit ID and firing rate.
    os.chdir(phy_folder[0])
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
    fs=30000;
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
    
    #End of for loop
    print("Stop the code here")



if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])
