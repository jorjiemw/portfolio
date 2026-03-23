import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------
# CREATE OUTPUT FOLDER
# -----------------------------
output_dir = Path("plots")
output_dir.mkdir(exist_ok=True)

# -----------------------------
# LOAD DATA
# -----------------------------
metadata = pd.read_csv("metadata.csv")
joint_velos = pd.read_csv("joint_velos.csv")
force_plate = pd.read_csv("force_plate.csv")
energy_flow = pd.read_csv("energy_flow.csv")

pitch_id = "session_pitch"
speed_col = "pitch_speed_mph"
level_col = "playing_level"
player_col = "user"
time_col = "time"

# -----------------------------
# JOINT VELOCITY COLUMNS
# -----------------------------
pelvis_col = "pelvis_velo_z"
torso_col = "torso_velo_z"
shoulder_col = "shoulder_velo_z"
elbow_col = "elbow_velo_z"

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def peak_abs(series):
    arr = pd.to_numeric(series, errors="coerce").to_numpy()
    if np.all(np.isnan(arr)):
        return np.nan
    return np.nanmax(np.abs(arr))

def get_peak_time(df, value_col, time_col="time"):
    tmp = df[[time_col, value_col]].copy()
    tmp[time_col] = pd.to_numeric(tmp[time_col], errors="coerce")
    tmp[value_col] = pd.to_numeric(tmp[value_col], errors="coerce")
    tmp = tmp.dropna()

    if tmp.empty:
        return np.nan

    idx = np.abs(tmp[value_col]).idxmax()
    return tmp.loc[idx, time_col]

# -----------------------------
# EXTRACT PEAK JOINT VELOCITIES
# -----------------------------
vel_features = (
    joint_velos.groupby(pitch_id)
    .agg(
        peak_pelvis_vel=(pelvis_col, peak_abs),
        peak_torso_vel=(torso_col, peak_abs),
        peak_shoulder_vel=(shoulder_col, peak_abs),
        peak_elbow_vel=(elbow_col, peak_abs),
    )
    .reset_index()
)

# -----------------------------
# EXTRACT PEAK TIMING + SEQUENCING
# -----------------------------
sequence_rows = []

for pid, sub in joint_velos.groupby(pitch_id):
    row = {pitch_id: pid}
    row["pelvis_peak_time"] = get_peak_time(sub, pelvis_col, time_col)
    row["torso_peak_time"] = get_peak_time(sub, torso_col, time_col)
    row["shoulder_peak_time"] = get_peak_time(sub, shoulder_col, time_col)
    row["elbow_peak_time"] = get_peak_time(sub, elbow_col, time_col)
    sequence_rows.append(row)

sequence_df = pd.DataFrame(sequence_rows)

sequence_df["pelvis_to_torso_delay"] = (
    sequence_df["torso_peak_time"] - sequence_df["pelvis_peak_time"]
)
sequence_df["torso_to_shoulder_delay"] = (
    sequence_df["shoulder_peak_time"] - sequence_df["torso_peak_time"]
)
sequence_df["shoulder_to_elbow_delay"] = (
    sequence_df["elbow_peak_time"] - sequence_df["shoulder_peak_time"]
)

# -----------------------------
# FORCE-PLATE FEATURES
# -----------------------------
force_features = (
    force_plate.groupby(pitch_id)
    .agg(
        peak_rear_force_z=("rear_force_z", peak_abs),
        peak_lead_force_z=("lead_force_z", peak_abs),
        peak_rear_force_x=("rear_force_x", peak_abs),
        peak_lead_force_x=("lead_force_x", peak_abs),
    )
    .reset_index()
)

# -----------------------------
# IMPULSE CALCULATION
# -----------------------------
impulse_rows = []

for pid, sub in force_plate.groupby(pitch_id):
    sub = sub.sort_values(time_col).copy()
    t = pd.to_numeric(sub[time_col], errors="coerce").to_numpy()
    rear_fz = pd.to_numeric(sub["rear_force_z"], errors="coerce").to_numpy()
    lead_fz = pd.to_numeric(sub["lead_force_z"], errors="coerce").to_numpy()

    valid_rear = ~(np.isnan(t) | np.isnan(rear_fz))
    valid_lead = ~(np.isnan(t) | np.isnan(lead_fz))

    rear_impulse_z = np.trapz(np.abs(rear_fz[valid_rear]), t[valid_rear]) if valid_rear.sum() > 1 else np.nan
    lead_impulse_z = np.trapz(np.abs(lead_fz[valid_lead]), t[valid_lead]) if valid_lead.sum() > 1 else np.nan

    impulse_rows.append({
        pitch_id: pid,
        "rear_impulse_z": rear_impulse_z,
        "lead_impulse_z": lead_impulse_z
    })

impulse_df = pd.DataFrame(impulse_rows)
force_features = force_features.merge(impulse_df, on=pitch_id, how="left")

# -----------------------------
# ENERGY FLOW FEATURES
# -----------------------------
energy_vars = [
    "rear_hip_energy_generated",
    "lead_hip_energy_generated",
    "shoulder_energy_generated",
    "elbow_energy_generated",
    "pelvis_thorax_seg_pwr",
    "thorax_dist_seg_pwr",
    "upper_arm_dist_seg_pwr",
    "forearm_dist_seg_pwr",
    "shoulder_energy_transfer_stp",
    "elbow_energy_transfer_stp",
]

energy_agg = {
    var: (var, peak_abs)
    for var in energy_vars
}

energy_features = (
    energy_flow.groupby(pitch_id)
    .agg(**energy_agg)
    .reset_index()
)

# -----------------------------
# EFFICIENCY RATIOS
# -----------------------------
energy_features["thorax_to_pelvis_power_ratio"] = (
    energy_features["thorax_dist_seg_pwr"] / energy_features["pelvis_thorax_seg_pwr"]
)

energy_features["arm_to_thorax_power_ratio"] = (
    energy_features["upper_arm_dist_seg_pwr"] / energy_features["thorax_dist_seg_pwr"]
)

energy_features.replace([np.inf, -np.inf], np.nan, inplace=True)

# -----------------------------
# MERGE EVERYTHING
# -----------------------------
analysis_df = (
    metadata[[pitch_id, player_col, level_col, speed_col]]
    .merge(vel_features, on=pitch_id, how="inner")
    .merge(sequence_df, on=pitch_id, how="left")
    .merge(force_features, on=pitch_id, how="inner")
    .merge(energy_features, on=pitch_id, how="inner")
)

print("Merged dataframe shape:", analysis_df.shape)

# -----------------------------
# VARIABLES TO TEST
# -----------------------------
vars_to_test = [
    "peak_pelvis_vel","peak_torso_vel","peak_shoulder_vel","peak_elbow_vel",
    "pelvis_to_torso_delay","torso_to_shoulder_delay","shoulder_to_elbow_delay",
    "peak_rear_force_z","peak_lead_force_z","peak_rear_force_x","peak_lead_force_x",
    "rear_impulse_z","lead_impulse_z",
    "rear_hip_energy_generated","lead_hip_energy_generated","shoulder_energy_generated","elbow_energy_generated",
    "pelvis_thorax_seg_pwr","thorax_dist_seg_pwr","upper_arm_dist_seg_pwr","forearm_dist_seg_pwr",
    "shoulder_energy_transfer_stp","elbow_energy_transfer_stp",
    "thorax_to_pelvis_power_ratio","arm_to_thorax_power_ratio"
]

# -----------------------------
# OVERALL CORRELATIONS
# -----------------------------
overall_results = []

for var in vars_to_test:
    sub = analysis_df[[var, speed_col]].dropna()
    corr = sub.corr().iloc[0, 1] if len(sub) >= 3 else np.nan

    overall_results.append({
        "variable": var,
        "correlation_with_pitch_speed": corr,
        "n": len(sub)
    })

overall_corr_df = pd.DataFrame(overall_results).sort_values(
    "correlation_with_pitch_speed", ascending=False
)

print("\n=== Overall Correlations ===")
print(overall_corr_df)

# -----------------------------
# CORRELATIONS BY LEVEL
# -----------------------------
level_results = []

for lvl in analysis_df[level_col].dropna().unique():
    level_sub = analysis_df[analysis_df[level_col] == lvl]

    for var in vars_to_test:
        sub = level_sub[[var, speed_col]].dropna()
        corr = sub.corr().iloc[0, 1] if len(sub) >= 3 else np.nan

        level_results.append({
            "level": lvl,
            "variable": var,
            "correlation_with_pitch_speed": corr,
            "n_pitches": len(sub)
        })

level_corr_df = pd.DataFrame(level_results)

# -----------------------------
# TOP VARIABLES BY LEVEL
# -----------------------------
top_by_level = (
    level_corr_df
    .sort_values(["level", "correlation_with_pitch_speed"], ascending=[True, False])
    .groupby("level")
    .head(5)
)

print("\n=== Top 5 Variables by Level ===")
print(top_by_level)

# -----------------------------
# TOP OVERALL VARIABLES
# -----------------------------
top_vars = overall_corr_df.dropna().head(8)["variable"].tolist()

print("\nTop variables by overall correlation:")
print(top_vars)


# -----------------------------
# SAVE PLOTS
# -----------------------------
for var in top_vars:
    plt.figure(figsize=(6, 5))

    for lvl in analysis_df[level_col].dropna().unique():
        sub = analysis_df[analysis_df[level_col] == lvl]
        plt.scatter(sub[var], sub[speed_col], label=lvl, alpha=0.6)

    plt.xlabel(var.replace("_", " ").title())
    plt.ylabel("Pitch Speed (mph)")
    plt.title(f"{var.replace('_', ' ').title()} vs Pitch Speed by Level")
    plt.legend()
    plt.tight_layout()

    filename = output_dir / f"{var}_vs_pitch_speed.png"
    plt.savefig(filename, dpi=150)
    plt.close()

print(f"\nPlots saved to: {output_dir.resolve()}")





