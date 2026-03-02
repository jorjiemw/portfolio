# Pitching Mechanics — Rotational Kinematic Sequence ⚾
### 📌 Project Overview

The concept of proximal-to-distal sequencing is foundational in baseball pitching biomechanics. Coaches and sports scientists often describe efficient pitching as a coordinated transfer of energy from:

Pelvis → Torso → Arm → Hand

While this principle is widely accepted, important questions remain:

Is this sequencing pattern consistently observed in real biomechanical data?

Does the timing between segment peaks matter more than peak magnitude?

Is sequencing variability related to ball velocity?

This project investigates rotational kinematic sequencing using Driveline Baseball’s open-source biomechanics dataset to better understand how segment timing and coordination relate to performance.
## Overview
This project provides tools to **analyze and visualize the rotational kinematic sequence** of baseball pitchers using sample joint angle CSV data from Driveline's Open Source Data. It plots **pelvis, torso, and throwing shoulder rotation** over time for each pitching session, and highlights the timing of **Maximum External Rotation (MER)** if available.

---

### 📈 Plot
[Rotational Sequence Plot](assets/session_1_rotational_sequence.png)

---

## 🔑 Features
-  **Session Splitting**  
   Supports datasets with `session_id` or automatic splitting when time resets to 0.  
-  **MER Detection**  
   Uses the `MER_time` column (in **seconds**) to mark the critical MER event.  
-  **Visualization**  
   Creates plots of pelvis, torso, and throwing shoulder rotation vs. time.  
   Annotates MER with a dashed vertical line when available.  
-  **Batch Processing**  
   Run on all sessions in a file or select a specific session.  
-  **Error Checking**  
   Detects missing or mislabeled columns and reports them clearly.

---

## 📂 Project Structure
- Pitching_Mechanics/
- ├─ README.md                 ← Project description (what it does, how to run it)
- ├─ src/                      
- │  ├─ pitching_mechanics.py  ← main script               
- ├─ assets/                   ← Plot
- │  ├─ session_1_rotational_sequence.png
- ├─ data/                    ← Small sample dataset 
- │  └─ pitching_joint_angles.csv
- ├─ requirements.txt         ← List of Python packages needed


### ▶️ Usage
1. **Install**
   python -m pip install numpy matplotlib pandas
2. **Modify Script**
python pitching_mechanics.py -i <csv_file> -o <output_dir> -s <session>
- Arguments:
- -i / --input : Path to dataset (e.g., data/pitching_joint_angles.csv)
- -o / --outdir : Folder to save generated plots (e.g., results/)
- -s / --session : all → Process all sessions or 1, 2, … → Specific session index
