# ⚾ Baseball Pitching Biomechanics Visualizer

### 📌 Overview
This project uses **a sample of motion capture landmark data** from Driveline's Open Source Biomechanics data to analyze and visualize pitching mechanics.  
It generates **3D skeleton animations** frame by frame, and splits recordings into **sessions** whenever the `time` column resets. 

---

### 🎥 Demo
![Pitching demo](assets/Session 1.gif)  

---

### 🔑 Features
- **3D Skeleton Animation**: Connects joints frame by frame to visualize pitching mechanics.  
- **Session Splitting**: Automatically detects when the `time` column resets to zero and creates a new session.  
- **Export**: Saves session as GIF or MP4 for easy sharing.  
- **Analysis Ready**: Prepares data for angle calculations (e.g., elbow flexion, shoulder rotation).  

---

### 📂 Project Structure
- project1_pitching/
- ├─ README.md          # Project description (what it does, how to run it)
- ├─ src/               # Code lives here
- │  ├─ animate_pitching.py   # main script for animation              
- ├─ assets/            # Pictures, GIFs, MP4s for README
- │  ├─ Session 1.gif
- ├─ data/              # Small sample dataset 
- │  └─ pitching_landmarks.csv
- ├─ requirements.txt   # List of Python packages needed

---

### ▶️ Usage

- **Run the script with:**
- python src/animate_pitching_simple.py --session 0
- **Arguments**
- --csv : Path to dataset (default: data/pitching_landmarks_sample.csv)
- --session : Session index to animate (default: 0)
- --fps : Frames per second (default: 30)
- --out : Output filename (default: session_<id>)
- Example:
- python src/animate_pitching_simple.py --csv data/pitching_landmarks_sample.csv --session 1 --fps 60 --out fast_throw
- This generates:
- fast_throw.mp4   # if ffmpeg available
- fast_throw.gif   # fallback if not

