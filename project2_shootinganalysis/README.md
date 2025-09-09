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

## 🚀 Quick Start

1. **Install**
   ```bash
   python -m pip install numpy matplotlib pandas
