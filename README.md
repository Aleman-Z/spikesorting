# spikesorting
Automatic and manual spike sorting based on SpikeInterface.

Dependencies: Same as [Spikeinterface](https://github.com/SpikeInterface/spiketutorials/tree/master/NWB_Developer_Breakout_Session_Sep2020)

For sort_tetrode.py install sorters as mentioned on this page:

https://spikeinterface.readthedocs.io/en/latest/sortersinfo.html

To be used on Linux :penguin:

-----------------------
## Spike sorting pipeline.

1.	Select trial/post-trial. This could also be a merged version of them.
2.	Fix file names by removing extra ‘_0’.  Run ‘fix_channel_name.py’.
3.	Group channels by tetrode and save them in a new folder for that tetrode.
4.	Activate the environment where SpikeInterface was installed and run the automatic spike sorter by going to terminal and typing:
```
python sort_tetrode_manual.py ‘complete_path_of_tetrode_folder’
```
5.	If you are running ‘sort_tetrode_manual.py’ the phy interface will pop up. Asking you to look at the detections from Klusta and discard the false positives. To discard the false positives select the unit from the Cluster view panel and press Alt+N. Save once you are done and close the interface.
6.	For either sort_tetrode or sort_tetrode_manual a phy folder will be created, were one can find the spike_times.npy and spike_clusters.npy files. By binarizing the spike times of each spike one can generate the activation matrix needed for the cell assembly analysis. This matrix is saved as ‘actmat_auto_tetrode#’.
7.	The ‘phy2assembly’ script will concatenate all activation matrices across tetrodes and then run the cell assembly detection.
