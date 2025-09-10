# Pitching Mechanics — Rotational Kinematic Sequence ⚾

## Overview
This project provides tools to **analyze and visualize the rotational kinematic sequence** of baseball pitchers using sample joint angle CSV data from Driveline's Open Source Data. It plots **pelvis, torso, and throwing shoulder rotation** over time for each pitching session, and highlights the timing of **Maximum External Rotation (MER)** if available.

---

## Features
- 📊 **Session Splitting**  
  - Supports datasets with `session_id` or automatic splitting when time resets to 0.  
- 🧮 **MER Detection**  
  - Uses the `MER_time` column (in **seconds**) to mark the critical MER event.  
- 🎨 **Visualization**  
  - Creates plots of pelvis, torso, and throwing shoulder rotation vs. time.  
  - Annotates MER with a dashed vertical line when available.  
- 💾 **Batch Processing**  
  - Run on all sessions in a file or select a specific session.  
- 🔎 **Error Checking**  
  - Detects missing or mislabeled columns and reports them clearly.

---

## Installation
Clone the repository:
```bash
git clone https://github.com/yourusername/pitching-mechanics.git
cd pitching-mechanics
