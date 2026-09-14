"""
Generate final closed-loop characterization plots.

Input:
    data/final_characterization.csv
    data/final_disturbance.csv

Output:
    images/final_step_response.png
    images/final_disturbance_response.png
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

CHAR_FILE = ROOT / "data" / "final_characterization.csv"
DIST_FILE = ROOT / "data" / "final_disturbance.csv"

IMAGE_DIR = ROOT / "images"
IMAGE_DIR.mkdir(exist_ok=True)


def load_csv(path):
    df = pd.read_csv(path)

    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(subset=["millis", "target_rpm", "rpm"])
    return df


# ---------------------------------------------------------
# Final setpoint characterization
# ---------------------------------------------------------

df = load_csv(CHAR_FILE)

active = df[df["target_rpm"] != 0]

if not active.empty:
    start_ms = active.iloc[0]["millis"]
else:
    start_ms = df.iloc[0]["millis"]

df["time_s"] = (df["millis"] - start_ms) / 1000.0

plt.figure(figsize=(11, 6))
plt.plot(
    df["time_s"],
    df["target_rpm"],
    linestyle="--",
    label="Target RPM",
)
plt.plot(
    df["time_s"],
    df["rpm"],
    label="Measured RPM",
)

plt.xlabel("Time (s)")
plt.ylabel("Speed (RPM)")
plt.title("Final PI Closed-Loop Speed Response")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

output_path = IMAGE_DIR / "final_step_response.png"
plt.savefig(output_path, dpi=200)
plt.close()

print(f"Saved {output_path}")


# ---------------------------------------------------------
# Disturbance test
# ---------------------------------------------------------

dist = load_csv(DIST_FILE)

active = dist[dist["target_rpm"] != 0]

if not active.empty:
    start_ms = active.iloc[0]["millis"]
else:
    start_ms = dist.iloc[0]["millis"]

dist["time_s"] = (dist["millis"] - start_ms) / 1000.0

fig, ax1 = plt.subplots(figsize=(11, 6))

ax1.plot(
    dist["time_s"],
    dist["target_rpm"],
    linestyle="--",
    label="Target RPM",
)

ax1.plot(
    dist["time_s"],
    dist["rpm"],
    label="Measured RPM",
)

ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Speed (RPM)")
ax1.grid(True, alpha=0.3)

ax2 = ax1.twinx()

ax2.plot(
    dist["time_s"],
    dist["output"],
    alpha=0.6,
    label="Controller Output",
)

ax2.set_ylabel("PWM Command")

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

ax1.legend(
    lines1 + lines2,
    labels1 + labels2,
    loc="best",
)

plt.title("PI Disturbance Response at 100 RPM")
fig.tight_layout()

output_path = IMAGE_DIR / "final_disturbance_response.png"
plt.savefig(output_path, dpi=200)
plt.close()

print(f"Saved {output_path}")