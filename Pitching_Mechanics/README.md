# Kinetic Chain Contributions to Pitch Velocity in Baseball Pitching

## Overview  

This project analyzes how different components of the kinetic chain contribute to pitch velocity using open-source biomechanics data. The goal is to quantify which biomechanical factors are most strongly associated with performance and examine how these relationships vary across playing levels.

The analysis focuses on:
- Force production (ground reaction forces)  
- Energy transfer through the body  
- Segmental angular velocities  

---

## Research Questions  

- What biomechanical variables are most strongly associated with pitch velocity?  
- Does performance depend more on force production, energy transfer, or segmental velocity?  
- What trends are observed across playing levels in this dataset?  

---

## Data  

- OpenBiomechanics baseball pitching dataset (Driveline)  
- Total pitches analyzed: **403**

### Sample Sizes by Playing Level
- College: **307**
- Independent: **41**
- High School: **32**
- MiLB: **23**

Data types used:
- Joint angular velocities  
- Force plate data  
- Energy flow / segment power data  
- Metadata (pitch speed, playing level)  

---

## Methods  

### Feature Extraction  

For each pitch:

**Segmental Velocity**
- Peak pelvis, torso, shoulder, and elbow angular velocities  

**Force Production**
- Peak ground reaction forces (vertical and horizontal)  
- Impulse  

**Energy Flow**
- Segment power (pelvis, torso, upper arm, forearm)  
- Energy generation and transfer  

---

### Analysis  

- Correlation analysis between biomechanical variables and pitch velocity  
- Comparison of relationships across playing levels  
- Identification of top contributing variables  

---

## Key Findings  

### 1. Energy Transfer Shows the Strongest Relationship with Pitch Velocity  

The strongest relationships with pitch velocity were observed in:

- Forearm segment power (r ≈ 0.69)  
- Upper arm segment power (r ≈ 0.66)  
- Thorax (trunk) segment power (r ≈ 0.63)  
- Shoulder energy transfer (r ≈ 0.52)  

These were consistently stronger than force production variables.

---

### 2. Distal Segment Output is Consistently Associated with Performance  

Across all playing levels, variables related to the arm (upper arm and forearm) showed the strongest relationships with pitch velocity.

Examples:
- High school forearm segment power: r ≈ 0.91 (n=32)  
- College forearm segment power: r ≈ 0.61 (n=307)  

This indicates that distal segment output reflects how effectively energy is transferred through the kinetic chain.

---

### 3. Force Production Shows Moderate Relationships  

Force-related variables demonstrated weaker relationships:

- Lead ground reaction force: r ≈ 0.40  
- Impulse variables: r ≈ 0.17–0.50 depending on level  

This suggests that while force production contributes to performance, it is not the strongest differentiating factor.

---

### 4. Trends Across Playing Levels  

Due to the imbalance in sample sizes, findings across levels should be interpreted as trends.

**College (n=307)**
- Strong and consistent relationships with energy transfer and distal segment power  
- Provides the most reliable estimates  

**High School (n=32) & Independent (n=41)**
- Similar patterns observed  
- Greater variability due to smaller sample sizes  

**MiLB (n=23)**
- Weaker relationships across individual variables  
- May reflect both smaller sample size and reduced variability at higher levels  

---

## Interpretation  

Pitch velocity is most strongly associated with variables representing trunk contribution and distal segment output, including thorax, upper arm, and forearm power (r ≈ 0.6–0.7). These variables reflect how effectively energy is transferred through the kinetic chain rather than isolated segment performance.

Force production variables showed weaker relationships, suggesting that generating force alone is not sufficient without effective transfer through the body.

At higher levels (MiLB), no single variable showed a strong relationship with pitch velocity. This suggests that performance differences at higher levels may depend more on the coordination of multiple components rather than any single biomechanical factor.

### Actionable Insights  

- Emphasize generating movement from the lower body and trunk rather than relying primarily on the arm  
- Focus on smooth transfer of energy from the hips and torso into the arm  
- High arm output without trunk contribution may indicate inefficient mechanics  
- Training should prioritize coordination and energy flow through the full kinetic chain in addition to strength development  

---

## Limitations  

- Unequal sample sizes across playing levels (college heavily represented)  
- Smaller sample sizes (e.g., MiLB n=23) may reduce stability of correlations  
- Correlation analysis does not account for interactions between variables  
- External factors (strength, fatigue, training background) not included  

---

## Future Work  

- Apply multivariate models to account for interactions between variables  
- Investigate nonlinear relationships  
- Develop metrics for energy transfer efficiency  
- Explore relationships between biomechanics and injury risk  

---

## Tools and Technologies  

- Python (Pandas, NumPy, Matplotlib)  
- Biomechanics data processing  
- Time-series feature extraction  

---

## Key Takeaway  

Pitch velocity is more strongly associated with how energy is transferred through the kinetic chain—particularly into the arm—than with force production alone. At higher levels, performance appears to depend on the coordination of multiple components rather than a single dominant factor.

## 📈 Plot
[Rotational Sequence Plot](assets/session_1_rotational_sequence.png)



