# spikesorting
Automatic and manual spike sorting based on SpikeInterface.

Dependencies: Same as [Spikeinterface](https://github.com/SpikeInterface/spiketutorials/tree/master/NWB_Developer_Breakout_Session_Sep2020)

For sort_tetrode.py install sorters as mentioned on this page:

https://spikeinterface.readthedocs.io/en/latest/sortersinfo.html


-----------------------
## Spike sorting pipeline.

1.	Select trial/post-trial. This could also be a merged version of them.
2.	Fix file names by removing extra ‘_0’.  Run ‘fix_channel_name.py’.
3.	Group channels by tetrode and save them in a new folder for that tetrode.
4.	Activate the environment where SpikeInterface was installed and run the automatic spike sorter by going to terminal and typing:
```
python sort_tetrode_manual.py ‘complete_path_of_tetrode_folder’
```
