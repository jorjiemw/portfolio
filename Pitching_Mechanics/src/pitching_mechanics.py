"""
Pitching Rotational Kinematic Sequence (MER_time in seconds, no fallback)

CLI (3 args):
  -i/--input   : CSV path
  -o/--outdir  : output folder for PNGs
  -s/--session : 'all' or a 1-based session number (e.g., 2)

Plots Pelvis, Torso, and Throwing Shoulder rotation vs time.
MER timing:
  * Uses 'MER_time' ONLY (per session), interpreted as SECONDS.
  * If MER_time missing/NaN in a session -> no MER line.
"""

import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---- fixed column names (edit if your headers differ) ----
TIME_COL = "time"
PELVIS_COL = "pelvis_angle_z"
TORSO_COL = "torso_angle_z"
THROWING_SHOULDER_ROT_COL = "shoulder_angle_z"  # your throwing shoulder rotation column
MER_TIME_COL = "MER_time"                       # time in SECONDS where MER occurs


def split_sessions(df: pd.DataFrame, tol: float = 1e-9):
    """Prefer 'session_id'; else split when time ~ 0."""
    if "session_id" in df.columns:
        groups = [g.copy().reset_index(drop=True) for _, g in df.groupby("session_id", sort=True)]
        labels = [str(k) for k, _ in df.groupby("session_id", sort=True).groups.items()]
        return groups, labels

    if TIME_COL not in df.columns:
        raise ValueError(f"Missing time column '{TIME_COL}' in CSV.")

    t = df[TIME_COL].to_numpy(dtype=float)
    starts = np.where(np.isclose(t, 0.0, atol=tol))[0].tolist()
    if not starts:
        return [df.copy().reset_index(drop=True)], ["1"]

    starts = sorted(starts) + [len(df)]
    sessions, labels = [], []
    for i in range(len(starts) - 1):
        s, e = starts[i], starts[i + 1]
        sessions.append(df.iloc[s:e].copy().reset_index(drop=True))
        labels.append(str(i + 1))
    return sessions, labels


def mer_time_seconds(session_df: pd.DataFrame):
    """
    Return MER time in SECONDS for this session from MER_time.
    - Uses the first non-NaN value (if repeated per frame, they’ll be identical).
    - No conversion, no fallback.
    """
    if MER_TIME_COL not in session_df.columns:
        return None
    vals = pd.to_numeric(session_df[MER_TIME_COL], errors="coerce").dropna().to_numpy()
    if vals.size == 0:
        return None
    return float(vals[0])  # already in seconds


def plot_session(sdf: pd.DataFrame, title: str, out_path: Path, mer_t: float | None, show: bool):
    required = [TIME_COL, PELVIS_COL, TORSO_COL, THROWING_SHOULDER_ROT_COL]
    missing = [c for c in required if c not in sdf.columns]
    if missing:
        raise ValueError(f"Missing columns in CSV: {missing}")

    t  = pd.to_numeric(sdf[TIME_COL], errors="coerce").to_numpy(dtype=float)
    yp = pd.to_numeric(sdf[PELVIS_COL], errors="coerce").to_numpy(dtype=float)
    yt = pd.to_numeric(sdf[TORSO_COL], errors="coerce").to_numpy(dtype=float)
    ys = pd.to_numeric(sdf[THROWING_SHOULDER_ROT_COL], errors="coerce").to_numpy(dtype=float)

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(t, yp, label="Pelvis Rotation")
    ax.plot(t, yt, label="Torso Rotation")
    ax.plot(t, ys, label="Throwing Shoulder Rotation")

    if mer_t is not None and np.isfinite(mer_t):
        ax.axvline(mer_t, color="k", linestyle="--", alpha=0.8, label=f"MER @ {mer_t:.3f}s")

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Rotation Angle (degrees)")
    ax.set_title(title)
    ax.legend(loc="best")
    fig.tight_layout()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    if show:
        plt.show()
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description="Plot rotational sequence by session (MER_time in seconds).")
    ap.add_argument("-i", "--input", required=True, help="Path to CSV (e.g., data/pitching_joint_angles.csv)")
    ap.add_argument("-o", "--outdir", required=True, help="Folder to save PNGs")
    ap.add_argument("-s", "--session", required=True, help="'all' or a 1-based session number (e.g., 2)")
    args = ap.parse_args()

    df = pd.read_csv(Path(args.input))
    sessions, labels = split_sessions(df)

    if args.session.lower() == "all":
        for lab, sess in zip(labels, sessions):
            mer_t = mer_time_seconds(sess)
            out_path = Path(args.outdir) / f"session_{lab}_rotational_sequence.png"
            plot_session(sess, f"Rotational Kinematic Sequence — Session {lab}", out_path, mer_t, show=False)
            print(f"Session {lab}: MER {'{:.3f}s'.format(mer_t) if mer_t is not None else 'N/A'} -> {out_path}")
        print(f"All plots saved to: {Path(args.outdir).resolve()}")
        return

    try:
        sel = int(args.session)
    except ValueError:
        raise SystemExit("Error: --session must be 'all' or an integer like 1, 2, ...")
    if sel < 1 or sel > len(sessions):
        raise SystemExit(f"Error: session {sel} is out of range (there are {len(sessions)} sessions).")

    sess = sessions[sel - 1]
    mer_t = mer_time_seconds(sess)
    out_path = Path(args.outdir) / f"session_{sel}_rotational_sequence.png"
    plot_session(sess, f"Rotational Kinematic Sequence — Session {sel}", out_path, mer_t, show=True)
    print(f"Session {sel}: MER {'{:.3f}s'.format(mer_t) if mer_t is not None else 'N/A'} -> {out_path}")


if __name__ == "__main__":
    main()
