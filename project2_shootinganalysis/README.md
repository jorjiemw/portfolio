# 🏀 Basketball Shooting Analysis

Analyze a basketball shot (e.g., free throw) from **Maple Leaf Sports & Entertainment's (MLSE) Sport Performance Lab (SPL) Open Free Throw Data JSON**.  
This toolkit computes **wrist, elbow, and knee flexion magnitudes**, detects **ball release** (“ball leaves the hand”), and saves **clean plots + a CSV**. 

---

## ✨ Features

- 📈 Plots **Right & Left**: Wrist, Elbow, Knee flexion magnitudes (deg)
- 🎯 **Release detection** (default = ball leaves hand) with **adaptive thresholds**
- 🧽 Optional smoothing & tiny-gap handling (advanced script)
- 🗂️ Exports **PNG** plots + a **CSV** table
- ⚙️ Works best at **30 fps** (supported in scripts)

---

### 📂 Project Structure
- project2_shootinganalysis/
- ├─ README.md          # Project description (what it does, how to run it)
- ├─ src/               # Code lives here
- │   ├─ shooting_mechanics.py   # main script for animation              
- ├─ assets/            # Pictures, GIFs, MP4s for README
- │   ├─ elbow_flexion_magnitude.png
-     ├─ wrist_flexion_magnitude.png
-     ├─ knee_flexion_magnitude.png
-     ├─ magnitudes_wrist_elbow_knee.csv
- ├─ data/              # JSON file from SPL Open Data 
-     └─ BB_FT_P0001_T0001.json

---

## 🚀 Quick Start

1. **Install**
   python -m pip install numpy matplotlib pandas
2. **Modify Script**
- INPUT_JSON    = r"C:\path\BB_FT_P0001_T0001 (1).json"  # ← your JSON file
- OUT_DIR       = r"C:\plots"                            # ← where to save outputs
- SHOOTING_SIDE = "R"                                    # or "L"
- FPS           = 30.0                                   # your recording frame rate
- SMOOTH_WIN    = 5                                      # 3–9; higher = smoother
