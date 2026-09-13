"""
Stage 5: PWM-vs-RPM characterization.

Reads a CSV logged by log_serial.py (columns: millis, duty, count, rpm),
splits it into the held-duty segments produced by the sweep, discards the
transient samples at the start of each segment, and reports the settled
RPM for each duty level on the way up and the way down.

Usage: python analyze_stage5.py <input.csv>
"""

import sys
import pandas as pd
import matplotlib.pyplot as plt

if len(sys.argv) < 2:
    print("Usage: python analyze_stage5.py <input.csv>")
    sys.exit(1)

infile = sys.argv[1]
df = pd.read_csv(infile)

# each contiguous run of identical 'duty' is one held command
df["segment"] = (df["duty"] != df["duty"].shift()).cumsum()

def settled_rpm(group):
    n = len(group)
    tail = group.iloc[n // 2:]   # back half of the segment - skip the transient
    return tail.median()

settled = df.groupby("segment").agg(
    duty=("duty", "first"),
    rpm=("rpm", settled_rpm),
    n_samples=("rpm", "size"),
).reset_index(drop=True)

# split at the peak: everything up to and including the max-duty segment
# is the ascending pass, everything from there onward is descending
peak_idx = settled["duty"].idxmax()
ascending = settled.loc[:peak_idx].reset_index(drop=True)
descending = settled.loc[peak_idx:].reset_index(drop=True)

print("Ascending pass (settled RPM by duty):")
print(ascending[["duty", "rpm", "n_samples"]].to_string(index=False))
print("\nDescending pass (settled RPM by duty):")
print(descending[["duty", "rpm", "n_samples"]].to_string(index=False))

print("\nAscending pass, RPM change per unit duty between consecutive points:")
for i in range(1, len(ascending)):
    d_duty = ascending["duty"].iloc[i] - ascending["duty"].iloc[i - 1]
    d_rpm = ascending["rpm"].iloc[i] - ascending["rpm"].iloc[i - 1]
    slope = d_rpm / d_duty if d_duty != 0 else float("nan")
    print(f"  duty {ascending['duty'].iloc[i-1]:>3} -> {ascending['duty'].iloc[i]:>3}:"
          f"  {slope:6.3f} RPM per duty count")

merged = ascending.merge(descending, on="duty", suffixes=("_up", "_down"))
merged = merged[merged["duty"] != ascending["duty"].max()]
merged["hysteresis"] = merged["rpm_down"] - merged["rpm_up"]

print("\nAscending vs descending RPM at matching duty (hysteresis check):")
print(merged[["duty", "rpm_up", "rpm_down", "hysteresis"]].to_string(index=False))

plt.figure(figsize=(7, 5))
plt.plot(ascending["duty"], ascending["rpm"], "o-", label="ascending")
plt.plot(descending["duty"], descending["rpm"], "s-", label="descending")
plt.xlabel("PWM duty (0-255)")
plt.ylabel("Settled RPM")
plt.title("PWM vs RPM - open-loop characterization")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("images/stage5_pwm_vs_rpm.png", dpi=150)
print("\nPlot saved to images/stage5_pwm_vs_rpm.png")