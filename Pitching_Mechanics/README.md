# Pitching Mechanics — Rotational Kinematic Sequence ⚾
# Kinetic Chain Contributions to Pitch Velocity in Baseball Pitching

## Overview  

This project analyzes how different components of the kinetic chain contribute to pitch velocity using Driveline's open-source biomechanics data. The goal is to identify which biomechanical factors most strongly influence performance and how these relationships differ across playing levels.

The analysis integrates:
- Force production (ground reaction forces)
- Energy transfer through the body
- Segmental angular velocities

---

## Research Questions  

- What biomechanical variables are most strongly associated with pitch velocity?  
- Does performance depend more on force production, energy transfer, or segmental velocity?  
- How do these relationships differ across playing levels (high school, college, professional)?  

---

## Data  

- OpenBiomechanics baseball pitching dataset (Driveline)  
- Data types used:
  - Joint angular velocities  
  - Force plate data  
  - Energy flow / segment power data  
  - Metadata (pitch speed, playing level)  

---

## Methods  

### Feature Extraction  

For each pitch, the following features were extracted:

**Segmental Velocity**
- Peak pelvis, torso, shoulder, and elbow angular velocities  

**Force Production**
- Peak ground reaction forces (vertical and horizontal)  
- Impulse (force over time)  

**Energy Flow**
- Segment power (pelvis, torso, upper arm, forearm)  
- Energy generated at joints  
- Energy transfer between segments  

---

### Analysis  

- Correlation analysis between biomechanical variables and pitch velocity  
- Comparison of results across playing levels  
- Identification of top contributing variables  

---

## Key Findings  

### 1. Energy Transfer is the Primary Driver of Pitch Velocity  

The strongest relationships with pitch velocity were observed in:

- Forearm segment power (r ≈ 0.69)  
- Upper arm segment power (r ≈ 0.66)  
- Thorax (trunk) segment power (r ≈ 0.63)  
- Shoulder energy transfer (r ≈ 0.52)  

These relationships were consistently stronger than those observed for force production or segmental velocity.

This indicates that pitch velocity is more strongly associated with how efficiently energy is transferred through the kinetic chain than with how much force is generated.

---

### 2. Distal Segment Output is Critical  

Across all playing levels, variables related to the arm (upper arm and forearm) consistently showed the highest correlations with pitch velocity.

For example:
- High school forearm segment power: r ≈ 0.91  
- College forearm segment power: r ≈ 0.61  

This suggests that effective transfer of energy into the distal segments is a key determinant of performance.

---

### 3. Force Production Plays a Secondary Role  

Ground reaction force and impulse variables showed moderate relationships with pitch velocity:

- Lead ground reaction force: r ≈ 0.40  
- Impulse variables: r ≈ 0.17–0.50 depending on level  

This indicates that while force production contributes to performance, it is not the primary limiting factor.

---

### 4. Differences Across Playing Levels  

**High School**
- Strong dependence on distal segment power  
- Greater reliance on arm-driven mechanics  

**College**
- Increased contribution from trunk (thorax power ≈ 0.61)  
- Improved energy transfer through the kinetic chain  

**MiLB**
- Lower correlations across individual variables  
- Suggests performance depends on multiple interacting factors rather than a single dominant variable  

---

## Interpretation  

Pitch velocity appears to be more strongly driven by how efficiently energy is transferred through the body—especially from the trunk into the arm—than by how much force is produced against the ground. While strength and force contribute to performance, the key difference lies in how effectively that energy is carried through the motion and expressed at the arm.

### Actionable Insights  

- Emphasize generating movement from the lower body and trunk rather than relying primarily on the arm  
- Focus on smooth, continuous energy transfer from the hips and torso into the arm  
- Heavy reliance on arm speed may indicate energy is not being effectively transferred earlier in the motion  
- Training should prioritize full-body coordination and movement efficiency in addition to strength development  
---

## Limitations  

- Correlation analysis does not capture nonlinear relationships  
- Unequal sample sizes across playing levels  
- External factors such as strength, fatigue, and training background were not included  

---

## Future Work  

- Investigate nonlinear relationships between biomechanics and performance  
- Develop efficiency metrics for energy transfer  
- Build predictive models for pitch velocity  
- Explore relationships between biomechanics and injury risk  

---

## Tools and Technologies  

- Python (Pandas, NumPy, Matplotlib)  
- Biomechanics data processing  
- Time-series feature extraction  

---

## Key Takeaway  

Pitch velocity appears to be driven less by how much force is produced and more by how efficiently energy is transferred through the kinetic chain, particularly into the distal segments of the arm.
## 📈 Plot
[Rotational Sequence Plot](assets/session_1_rotational_sequence.png)


## ▶️ Usage
1. **Install**
   python -m pip install numpy matplotlib pandas
2. **Modify Script**
python pitching_mechanics.py -i <csv_file> -o <output_dir> -s <session>
- Arguments:
- -i / --input : Path to dataset (e.g., data/pitching_joint_angles.csv)
- -o / --outdir : Folder to save generated plots (e.g., results/)
- -s / --session : all → Process all sessions or 1, 2, … → Specific session index
