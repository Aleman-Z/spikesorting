# 🧠 SpikeSorting: Object Space Task Pipeline

**Automatic and manual spike sorting for tetrode recordings** using [SpikeInterface (2020 version)](https://github.com/SpikeInterface/spiketutorials/blob/master/old_api/NWB_Developer_Breakout_Session_Sep2020/environment.yml).

<p align="center">
<img src="cover.JPG" width="600">
</p>
<p align="center">
<img src="pipeline.PNG" width="1000">
</p>

---

## ⚠️ Compatibility Warning

> This pipeline was built using SpikeInterface from 2020. **Newer versions are not guaranteed to be compatible.**  
> Make sure to install the sorters as described [here](https://spikeinterface.readthedocs.io/en/latest/install_sorters.html).

For troubleshooting, refer to these [installation instructions (PDF)](https://github.com/Aleman-Z/spikesorting/blob/main/spikesorting-setup.pdf).

---

## 📦 Dependencies

- [SpikeInterface (2020)](https://github.com/SpikeInterface/spiketutorials/blob/master/old_api/NWB_Developer_Breakout_Session_Sep2020/environment.yml)
- Matlab (for merging scripts)
- Linux recommended :penguin:

To use Matlab-based sorters:
- Place them in: `~/Documents/SpikeSorting/`
- Add the path in your terminal:
  ```bash
  export PYTHONPATH=$PYTHONPATH:/path/to/this/folder
  ```
  Or add it permanently via `gedit ~/.bashrc`.

---

## 🔁 Pipeline Overview

### Step 1: Activate Environment
```bash
conda activate <your_spikeinterface_env>
```

---

### Step 2: Check for Corrupted Files
```bash
python -m check_length 'path_to_folder_with_Study_day_subfolders'
```
**Make sure**: No duplicate `.continuous` files (e.g., `CH1.continuous` and `CH1_2.continuous`) in the same folder.

---

### Step 3: Merge Trials (Matlab)

- Use `merge_channels_revised_T1_PT1.m` or `merge_channels_revised.m` scripts.
- **Important**: Use correct sampling rate (`20kHz` vs `30kHz`). Refer to the Excel sheet:  
  `RAT_OS_EPHYS_Channel_Normalization_Across_Animals.xlsx`.

You’ll need two merged versions:
1. T1 + PT1
2. Entire day (Pre + T1 + PT1 + T2 + PT2 + ...)

Check the [Google planning sheet](https://docs.google.com/spreadsheets/d/1FvTOxkV9HDviEM8qUjApdJ_2NViZCOhmVhzIALzLDKA/edit#gid=949291845) for animal-specific notes.

Create:
- `hpc.xlsx` and/or `cortex.xlsx` with tetrode IDs and channels.

---

### Step 4: Fix Channel Names
```bash
python -m fix_channel_name 'path_to_.continuous_files'
```

Copy the following into the merged folder (from same study day):
- `all_channels.events`
- `Continuous_Data.openephys`
- `messages.events`
- `settings.xml`
- [`tetrode.prb`](https://github.com/Aleman-Z/spikesorting/blob/main/tetrode.prb) (Use same file for all)
- `hpc.xlsx`, `cortex.xlsx` (as needed)

---

### Step 5: Rearrange by Tetrode
```bash
python -m rearrange_folders 'path_to_merged_folder'
```
- Set `folders=['cortex']` if not sorting hippocampus.

---

### Step 6: Run Automatic Spike Sorting
#### Recommended: Use Spyder
```bash
conda activate spiketutorial
spyder
```
- Load `run_tetrodes.py`
- Edit the `folder` variable.
- Press `Ctrl+A` then `F9` to run.

Or from terminal:
```bash
python -m run_tetrodes 'path_to_brain_area_folder'
```

To generate consensus JSON (after T1+PT1 sorting):
```bash
python -m create_json 'path_to_brain_area_folder'
```

To run on full-day:
```bash
python -m run_tetrodes 'path_to_full_day_folder'
```

---

### Step 7: Manual Curation with Phy
```bash
python -m run_tetrodes_manual 'path_to_tetrode_folder'
```
Phy interface:
- `Alt+N` = noise
- `Alt+M` = MUA
- `Alt+G` = pyramidal
- Interneurons = unlabeled

**Important**: Save before closing Phy interface!

---

### Step 8: Spike Times and Activation Matrix
- Output: `spike_times.npy`, `spike_clusters.npy`, `actmat_auto_tetrode#`
- Binning: 25 ms

---

### Step 9: Cell Assembly Detection
```bash
python -m phy2assembly
```

---

### Step 10: View & Export Sorter Results

- Load into Phy:
```bash
os.system('phy template-gui phy_AGR/params.py')
```

- After manual curation:
```bash
python -m consensus_post_curation 'path_to_tetrode_folder'
```

- View sorter results:
```bash
python -m view_sorter_detections
```

---

### Step 11: Quality Metrics
```bash
conda env create -f environment_qm.yml
conda activate spiketutorial_qm

python -m quality_metrics
```

---

## 🧪 Extra Options

### 🐧 Linux: Fast Auto-Sorting (Adrian’s PC)
```bash
./loop
```
- Make sure `loop` is in your PATH.
- Modify the `sorter.py` functions (`ms4`, `auto`) to include `_exit()`.

[loop.sh file](https://github.com/Aleman-Z/spikesorting/blob/main/loop%20(copy))  
Rename from `loop (copy)` → `loop`

---

## 🧯 Troubleshooting Open Ephys Corrupted Files

You may need to modify:
- `openephys_tools.py`: [see lines here](https://github.com/Aleman-Z/spikesorting/blob/main/openephys_tools.py#L49-L85)
- `core.py`: [see lines here](https://github.com/Aleman-Z/spikesorting/blob/main/core.py#L723-L727)

Path:
```
~/anaconda3/envs/spiketutorial/lib/python3.6/site-packages/pyopenephys
```

---

## 🆕 New Scripts (TBD)
Descriptions pending:
- `run_tetrodes_brain_areas.py`
- `run_tetrodes_json.py`
- `run_tetrodes_loop.py`
- `truncate2.py`
