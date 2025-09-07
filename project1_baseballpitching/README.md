# ⚾ Baseball Pitching Biomechanics Visualizer

### 📌 Overview
This project uses **sample of motion capture landmark data** from Driveline's Open Source Biomechanics data to analyze and visualize pitching mechanics.  
It generates **3D skeleton animations** frame by frame, and splits recordings into **sessions** whenever the `time` column resets. 

---

### 🎥 Demo
![Pitching demo](assets/pitching_demo.gif)  
*(Add your exported GIF or MP4 screenshot here — put the file in the `assets/` folder and update the link.)*

---

### 🔑 Features
- **3D Skeleton Animation**: Connects joints frame by frame to visualize pitching mechanics.  
- **Session Splitting**: Automatically detects when the `time` column resets to zero and creates a new session.  
- **Export**: Saves session as GIF or MP4 for easy sharing.  
- **Analysis Ready**: Prepares data for angle calculations (e.g., elbow flexion, shoulder rotation).  

---

### 📂 Project Structure
