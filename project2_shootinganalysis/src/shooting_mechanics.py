# ===== Simple Free-Throw Plots (Auto release: ball leaves hand) =====
INPUT_JSON = r"C:/Users/Kesar Lab/Desktop/Py Projects/BB_FT_P0001_T0001.json"
OUT_DIR    = r"C:/Users/Kesar Lab/Desktop/Py Projects/plots_out"      # or None -> creates ./plots next to this script
SHOOTING_SIDE = "R"           # "R" or "L"
FPS = 30.0                    # frames per second
SMOOTH_WIN = 5                # frames for light smoothing (0/1 disables)
# ===================================================================

import os, json, math
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from csv import writer as csv_writer

def _to_xyz(v):
    try:
        x,y,z = v; return np.array([float(x), float(y), float(z)], float)
    except: return np.array([np.nan, np.nan, np.nan], float)

def midpoint(a,b):
    if a is None or b is None: return np.full(3, np.nan)
    if np.any(~np.isfinite(a)) or np.any(~np.isfinite(b)): return np.full(3, np.nan)
    return 0.5*(a+b)

def first_valid(*arrs):
    for a in arrs:
        if a is not None and np.any(np.isfinite(a)): return a
    return np.full(3, np.nan)

def angle_mag_deg(u, v):
    if u is None or v is None: return np.nan
    if np.any(~np.isfinite(u)) or np.any(~np.isfinite(v)): return np.nan
    nu, nv = np.linalg.norm(u), np.linalg.norm(v)
    if nu == 0 or nv == 0: return np.nan
    dot = float(np.dot(u, v))
    crs = float(np.linalg.norm(np.cross(u, v)))
    return math.degrees(math.atan2(crs, dot))  # 0..180

def simple_nan_interp(y):
    y = np.asarray(y, float)
    n = y.size; idx = np.arange(n)
    m = np.isfinite(y)
    if m.sum() == 0: return y
    y[~m] = np.interp(idx[~m], idx[m], y[m])
    return y

def smooth(y, win):
    if win is None or win <= 1: return y
    y = simple_nan_interp(y)
    k = np.ones(int(win))/max(1,int(win))
    return np.convolve(y, k, mode="same")

def read_trial(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    track = data.get("tracking", [])
    frames, times_ms, ball = [], [], []
    R_SH=[]; L_SH=[]; R_EL=[]; L_EL=[]; R_WR=[]; L_WR=[]
    R_HP=[]; L_HP=[]; R_KN=[]; L_KN=[]; R_AN=[]; L_AN=[]
    R_F1=[]; R_F5=[]; L_F1=[]; L_F5=[]
    for fr in track:
        frames.append(fr.get("frame", np.nan))
        times_ms.append(fr.get("time", np.nan))
        d = fr.get("data", {}) or {}
        p = d.get("player", {}) or {}
        ball.append(_to_xyz(d.get("ball", [])))
        R_SH.append(_to_xyz(p.get("R_SHOULDER")));  L_SH.append(_to_xyz(p.get("L_SHOULDER")))
        R_EL.append(_to_xyz(p.get("R_ELBOW")));     L_EL.append(_to_xyz(p.get("L_ELBOW")))
        R_WR.append(_to_xyz(p.get("R_WRIST")));     L_WR.append(_to_xyz(p.get("L_WRIST")))
        R_HP.append(_to_xyz(p.get("R_HIP")));       L_HP.append(_to_xyz(p.get("L_HIP")))
        R_KN.append(_to_xyz(p.get("R_KNEE")));      L_KN.append(_to_xyz(p.get("L_KNEE")))
        R_AN.append(_to_xyz(p.get("R_ANKLE")));     L_AN.append(_to_xyz(p.get("L_ANKLE")))
        R_F1.append(_to_xyz(p.get("R_1STFINGER"))); R_F5.append(_to_xyz(p.get("R_5THFINGER")))
        L_F1.append(_to_xyz(p.get("L_1STFINGER"))); L_F5.append(_to_xyz(p.get("L_5THFINGER")))
    frames = np.asarray(frames, float)
    times_s = np.asarray(times_ms, float)/1000.0
    ball = np.asarray(ball, float)
    R_SH=np.asarray(R_SH); L_SH=np.asarray(L_SH)
    R_EL=np.asarray(R_EL); L_EL=np.asarray(L_EL)
    R_WR=np.asarray(R_WR); L_WR=np.asarray(L_WR)
    R_HP=np.asarray(R_HP); L_HP=np.asarray(L_HP)
    R_KN=np.asarray(R_KN); L_KN=np.asarray(L_KN)
    R_AN=np.asarray(R_AN); L_AN=np.asarray(L_AN)
    R_F1=np.asarray(R_F1); R_F5=np.asarray(R_F5)
    L_F1=np.asarray(L_F1); L_F5=np.asarray(L_F5)
    HAND_R = np.array([midpoint(R_F1[i], R_F5[i]) if (np.any(np.isfinite(R_F1[i])) and np.any(np.isfinite(R_F5[i])))
                       else first_valid(R_F1[i], R_F5[i]) for i in range(len(frames))], float)
    HAND_L = np.array([midpoint(L_F1[i], L_F5[i]) if (np.any(np.isfinite(L_F1[i])) and np.any(np.isfinite(L_F5[i])))
                       else first_valid(L_F1[i], L_F5[i]) for i in range(len(frames))], float)
    return {
        "frames": frames, "times_s": times_s, "ball": ball,
        "R_SH": R_SH, "L_SH": L_SH, "R_EL": R_EL, "L_EL": L_EL, "R_WR": R_WR, "L_WR": L_WR,
        "R_HP": R_HP, "L_HP": L_HP, "R_KN": R_KN, "L_KN": L_KN, "R_AN": R_AN, "L_AN": L_AN,
        "HAND_R": HAND_R, "HAND_L": HAND_L
    }

def mags_from(D):
    N = len(D["frames"])
    EL_R = np.full(N, np.nan); EL_L = np.full(N, np.nan)
    KN_R = np.full(N, np.nan); KN_L = np.full(N, np.nan)
    WR_R = np.full(N, np.nan); WR_L = np.full(N, np.nan)
    for i in range(N):
        EL_R[i] = angle_mag_deg(D["R_SH"][i]-D["R_EL"][i], D["R_WR"][i]-D["R_EL"][i])
        EL_L[i] = angle_mag_deg(D["L_SH"][i]-D["L_EL"][i], D["L_WR"][i]-D["L_EL"][i])
        KN_R[i] = angle_mag_deg(D["R_HP"][i]-D["R_KN"][i], D["R_AN"][i]-D["R_KN"][i])
        KN_L[i] = angle_mag_deg(D["L_HP"][i]-D["L_KN"][i], D["L_AN"][i]-D["L_KN"][i])
        WR_R[i] = angle_mag_deg(D["R_EL"][i]-D["R_WR"][i], D["HAND_R"][i]-D["R_WR"][i])
        WR_L[i] = angle_mag_deg(D["L_EL"][i]-D["L_WR"][i], D["HAND_L"][i]-D["L_WR"][i])
    return {
        "ELBOW_R": 180.0 - EL_R, "ELBOW_L": 180.0 - EL_L,
        "KNEE_R":  180.0 - KN_R, "KNEE_L":  180.0 - KN_L,
        "WRIST_R": 180.0 - WR_R, "WRIST_L": 180.0 - WR_L,
    }

def auto_release(time_s, ball_xyz, wrist_xyz, fps=FPS, smooth_win=SMOOTH_WIN):
    """Adaptive 'ball leaves hand' based on wrist–ball distance."""
    t = np.asarray(time_s, float)
    d = np.linalg.norm(ball_xyz - wrist_xyz, axis=1)
    ds = smooth(d, smooth_win if smooth_win else 1)

    # stats → adaptive thresholds
    finite = np.isfinite(ds)
    if finite.sum() < 5: return None
    dmin = float(np.nanmin(ds[finite]))
    d90  = float(np.nanpercentile(ds[finite], 90))
    spread = max(1e-6, d90 - dmin)

    contact_r = dmin + 0.15*spread          # slightly above tight contact
    rise_delta = max(0.01, 0.06*spread)     # must keep separating a bit
    stay_n = max(2, int(round(100 * fps / 1000.0)))  # ≈100 ms

    N = len(ds)
    for i in range(1, N - stay_n):
        if not (np.isfinite(ds[i-1]) and np.isfinite(ds[i])): continue
        crossed = (ds[i-1] < contact_r) and (ds[i] >= contact_r)
        if not crossed: continue
        seg = ds[i:i+stay_n+1]
        if np.all(np.isfinite(seg)) and np.all(seg >= contact_r) and (seg[-1] - seg[0] >= rise_delta):
            return i

    # Fallback: after global min, first frame that rises by rise_delta and stays higher
    k0 = int(np.nanargmin(ds[finite]))
    for j in range(k0+1, N - stay_n):
        seg = ds[j:j+stay_n+1]
        if np.all(np.isfinite(seg)) and (seg[-1] - ds[k0] >= rise_delta) and np.all(np.diff(seg) >= -1e-6):
            return j
    return None

def plot_pair(time_s, yR, yL, ylabel, title, out_png, release_t=None, smooth_win=SMOOTH_WIN):
    yR = np.asarray(yR, float); yL = np.asarray(yL, float)
    if smooth_win and smooth_win > 1:
        yR = smooth(yR, smooth_win); yL = smooth(yL, smooth_win)
    fig, ax = plt.subplots(figsize=(11,6))
    ax.plot(time_s, yR, label="Right"); ax.plot(time_s, yL, label="Left")
    if release_t is not None:
        ax.axvline(release_t, color="k", linestyle=":", label=f"Release ~ {release_t:.2f}s")
    ax.set_xlabel("time (s)"); ax.set_ylabel(ylabel); ax.set_title(title); ax.legend()
    fig.tight_layout(); fig.savefig(out_png, dpi=150); plt.close(fig)

def save_csv(path_csv, time_s, mags):
    headers = ["time_s","WRIST_R","WRIST_L","ELBOW_R","ELBOW_L","KNEE_R","KNEE_L"]
    rows = zip(time_s, mags["WRIST_R"], mags["WRIST_L"], mags["ELBOW_R"], mags["ELBOW_L"], mags["KNEE_R"], mags["KNEE_L"])
    with open(path_csv, "w", newline="", encoding="utf-8") as f:
        w = csv_writer(f); w.writerow(headers); w.writerows(rows)

def main():
    out_dir = Path(OUT_DIR) if OUT_DIR else (Path.cwd() / "plots")
    out_dir.mkdir(parents=True, exist_ok=True)

    D = read_trial(INPUT_JSON)
    time_s = np.asarray(D["frames"], float) / float(FPS)

    wrist = D["R_WR"] if SHOOTING_SIDE.upper()=="R" else D["L_WR"]
    rel_idx = auto_release(time_s, D["ball"], wrist, fps=FPS)
    release_t = float(time_s[rel_idx]) if rel_idx is not None else None

    mags = mags_from(D)
    plot_pair(time_s, mags["WRIST_R"], mags["WRIST_L"], "Wrist flexion magnitude (deg)",
              "Wrist flexion magnitude (R & L)", str(out_dir/"wrist_flexion_magnitude.png"), release_t)
    plot_pair(time_s, mags["ELBOW_R"], mags["ELBOW_L"], "Elbow flexion magnitude (deg)",
              "Elbow flexion magnitude (R & L)", str(out_dir/"elbow_flexion_magnitude.png"), release_t)
    plot_pair(time_s, mags["KNEE_R"], mags["KNEE_L"], "Knee flexion magnitude (deg)",
              "Knee flexion magnitude (R & L)", str(out_dir/"knee_flexion_magnitude.png"), release_t)

    save_csv(str(out_dir/"magnitudes_wrist_elbow_knee.csv"), time_s, mags)
    print("Saved to:", str(out_dir.resolve()))
    print("Release:", f"{release_t:.3f} s (frame {rel_idx})" if release_t is not None else "NOT DETECTED")

if __name__ == "__main__":
    main()



