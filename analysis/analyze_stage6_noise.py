"""
Stage 6: check whether RPM filtering is actually needed.

Uses the Stage 5 PWM sweep data and looks at the settled RPM samples
for each duty segment.

Usage:
    python3 analysis/analyze_stage6_noise.py data/stage5_pwm_sweep.csv
"""

import sys
import pandas as pd

if len(sys.argv) < 2:
    print("Usage: python3 analysis/analyze_stage6_noise.py <input.csv>")
    sys.exit(1)

infile = sys.argv[1]
df = pd.read_csv(infile)

# Each continuous run of the same duty value is one segment.
df["segment"] = (df["duty"] != df["duty"].shift()).cumsum()


def noise_stats(group):
    n = len(group)

    # Use only the back half so the motor has time to settle.
    tail = group.iloc[n // 2:]

    return pd.Series({
        "duty": group["duty"].iloc[0],
        "mean_rpm": tail["rpm"].mean(),
        "std_rpm": tail["rpm"].std(),
        "min_rpm": tail["rpm"].min(),
        "max_rpm": tail["rpm"].max(),
        "n_samples": len(tail),
    })


stats = df.groupby("segment").apply(noise_stats).reset_index(drop=True)

stats["pct_std"] = (
    stats["std_rpm"] / stats["mean_rpm"].abs()
) * 100

stats["pk_pk"] = stats["max_rpm"] - stats["min_rpm"]

print(
    stats[
        ["duty", "mean_rpm", "std_rpm", "pct_std", "pk_pk", "n_samples"]
    ].to_string(index=False)
)

moving = stats[stats["mean_rpm"].abs() > 1.0]

print(
    f"\nWorst-case std as % of mean RPM while moving: "
    f"{moving['pct_std'].max():.2f}%"
)

print(
    f"Worst-case peak-to-peak spread: "
    f"{stats['pk_pk'].max():.2f} RPM"
)