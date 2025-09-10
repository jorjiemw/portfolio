import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter, PillowWriter
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (needed for 3D)
import matplotlib as mpl

# Try to use ffmpeg via imageio-ffmpeg if available (for MP4)
try:
    import imageio_ffmpeg
    mpl.rcParams["animation.ffmpeg_path"] = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    pass  # if this fails, MP4 save may still work if ffmpeg is on PATH

# -----------------------------
# Helpers
# -----------------------------
def add_session_id(df, time_col="time"):
    if time_col not in df.columns:
        raise KeyError(f"Expected a '{time_col}' column in the CSV.")
    t = pd.to_numeric(df[time_col], errors="coerce").ffill().fillna(0.0)
    resets = (t.diff() < 0) | ((t == 0) & (t.index != t.index.min()))
    return resets.cumsum().astype(int)  # 0-based internal IDs

def clean_chunk_dropna(chunk):
    """Drop frames that have NaN in any coordinate column (*_x, *_y, *_z)."""
    coord_cols = [c for c in chunk.columns if c.endswith(("_x", "_y", "_z"))]
    before = len(chunk)
    chunk = chunk.dropna(subset=coord_cols).reset_index(drop=True)
    removed = before - len(chunk)
    if removed > 0:
        print(f"[INFO] Dropped {removed} frame(s) with NaNs in coordinate columns.")
    return chunk

def safe_axis_limits(chunk, suffix):
    cols = [c for c in chunk.columns if c.endswith(suffix)]
    if not cols:
        return (-1.0, 1.0)
    arr = chunk[cols].to_numpy(dtype=float)
    arr = arr[~np.isnan(arr)]
    if arr.size == 0:
        return (-1.0, 1.0)
    return float(arr.min()), float(arr.max())

# -----------------------------
# Main
# -----------------------------
def main():
    parser = argparse.ArgumentParser(description="Animate pitching landmarks (choose session, remove NaNs).")
    here = os.path.dirname(os.path.abspath(__file__))
    parser.add_argument("--csv", default=os.path.join(here, "pitching_landmarks.csv"),
                        help="Path to landmarks CSV (default: ./pitching_landmarks.csv)")
    parser.add_argument("--time-col", default="time", help="Time column name (default: time)")
    parser.add_argument("--session", type=int, default=1,
                        help="1-based session number to animate (1 = first)")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second (default: 30)")
    parser.add_argument("--out", default=None,
                        help="Output base name without extension (default: session_<N> in the CSV folder)")
    args = parser.parse_args()

    # Load CSV
    if not os.path.exists(args.csv):
        raise FileNotFoundError(f"CSV not found at: {args.csv}")
    df = pd.read_csv(args.csv)

    # Add session_id and pick session
    df["session_id"] = add_session_id(df, time_col=args.time_col)
    groups = list(df.groupby("session_id"))
    if not groups:
        raise RuntimeError("No sessions detected. Check your time column and values.")

    n_sessions = len(groups)
    if args.session < 1 or args.session > n_sessions:
        raise IndexError(f"Requested session {args.session} out of range (1..{n_sessions}).")

    # Map 1-based CLI to 0-based internal index
    idx0 = args.session - 1
    sid0, chunk = groups[idx0]          # 0-based internal
    session_label = args.session        # 1-based for titles/files
    chunk = chunk.reset_index(drop=True)

    # Remove NaN frames from the selected session
    chunk = clean_chunk_dropna(chunk)
    if len(chunk) == 0:
        raise RuntimeError("All frames were dropped due to NaNs; nothing to animate.")

    # Skeleton connections (edit if your column names differ)
    connections = [
        ("glove_shoulder_jc", "glove_elbow_jc"),
        ("glove_elbow_jc", "glove_wrist_jc"),
        ("glove_wrist_jc", "glove_hand_jc"),
        ("shoulder_jc", "elbow_jc"),
        ("elbow_jc", "wrist_jc"),
        ("wrist_jc", "hand_jc"),
        ("glove_shoulder_jc", "shoulder_jc"),
        ("glove_shoulder_jc", "lead_hip"),
        ("shoulder_jc", "rear_hip"),
        ("lead_hip", "rear_hip"),
        ("rear_hip", "rear_knee_jc"),
        ("rear_knee_jc", "rear_ankle_jc"),
        ("lead_hip", "lead_knee_jc"),
        ("lead_knee_jc", "lead_ankle_jc"),
    ]

    # Figure/artists
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    scat = ax.scatter([], [], [], s=20)
    lines = [ax.plot([], [], [], "o-", lw=2)[0] for _ in connections]

    # Axis limits
    x_min, x_max = safe_axis_limits(chunk, "_x")
    y_min, y_max = safe_axis_limits(chunk, "_y")
    z_min, z_max = safe_axis_limits(chunk, "_z")

    def set_axes():
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.set_zlim(z_min, z_max)
        ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
        # Equal-ish aspect
        try:
            span = max(x_max - x_min, y_max - y_min, z_max - z_min)
            cx, cy, cz = (x_min + x_max)/2, (y_min + y_max)/2, (z_min + z_max)/2
            ax.set_xlim(cx - span/2, cx + span/2)
            ax.set_ylim(cy - span/2, cy + span/2)
            ax.set_zlim(cz - span/2, cz + span/2)
        except Exception:
            pass

    def init():
        set_axes()
        scat._offsets3d = ([], [], [])
        for ln in lines:
            ln.set_data([], [])
            ln.set_3d_properties([])
        return (scat, *lines)

    def update(frame):
        bases = [c[:-2] for c in chunk.columns if c.endswith("_x")]
        J = {}
        for base in bases:
            x, y, z = f"{base}_x", f"{base}_y", f"{base}_z"
            if x in chunk and y in chunk and z in chunk:
                xv, yv, zv = chunk.at[frame, x], chunk.at[frame, y], chunk.at[frame, z]
                if pd.notna(xv) and pd.notna(yv) and pd.notna(zv):
                    J[base] = (float(xv), float(yv), float(zv))
        if not J:
            return (scat, *lines)

        xs, ys, zs = zip(*J.values())
        scat._offsets3d = (xs, ys, zs)

        for ln, (j1, j2) in zip(lines, connections):
            if j1 in J and j2 in J:
                ln.set_data([J[j1][0], J[j2][0]], [J[j1][1], J[j2][1]])
                ln.set_3d_properties([J[j1][2], J[j2][2]])
            else:
                ln.set_data([], [])
                ln.set_3d_properties([])

        ax.set_title(f"Session {session_label} · Frame {frame}")
        return (scat, *lines)

    ani = animation.FuncAnimation(fig, update, frames=len(chunk), init_func=init,
                                  interval=1000/args.fps, blit=False)

    # Output filenames (use 1-based label in names)
    base = args.out or f"Session_{session_label}"
    out_dir = os.path.dirname(os.path.abspath(args.csv))
    mp4_path = os.path.join(out_dir, f"{base}.mp4")
    gif_path = os.path.join(out_dir, f"{base}.gif")

    # --- Save BOTH MP4 and GIF ---
    mp4_ok = gif_ok = False

    # MP4
    try:
        print("[INFO] Saving MP4…")
        writer_mp4 = FFMpegWriter(fps=args.fps, codec="libx264", bitrate=1800)
        ani.save(mp4_path, writer=writer_mp4, dpi=120)
        print(f"[OK] MP4 saved → {mp4_path}")
        mp4_ok = True
    except Exception as e:
        print(f"[WARN] MP4 save failed: {e}")

    # GIF
    try:
        print("[INFO] Saving GIF…")
        writer_gif = PillowWriter(fps=args.fps)
        ani.save(gif_path, writer=writer_gif, dpi=120)
        print(f"[OK] GIF saved → {gif_path}")
        gif_ok = True
    except Exception as e:
        print(f"[WARN] GIF save failed: {e}")

    if not mp4_ok and not gif_ok:
        raise RuntimeError("Both MP4 and GIF saves failed. Ensure ffmpeg (for MP4) and pillow are available.")

    plt.close(fig)

if __name__ == "__main__":
    main()
