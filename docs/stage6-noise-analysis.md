# Stage 6 — RPM Noise Analysis

## Goal

Determine whether the raw RPM measurement is noisy enough to justify adding a velocity filter before closed-loop control.

## Method

The existing Stage 5 sweep data was reused:

`data/stage5_pwm_sweep.csv`

For each constant-duty segment, only the back half of the samples was analyzed so the motor had time to settle.

The script:

`analysis/analyze_stage6_noise.py`

calculated:

- mean RPM
- standard deviation
- minimum RPM
- maximum RPM
- peak-to-peak RPM spread
- standard deviation as a percentage of mean RPM

## Results

For the motor while actually rotating:

- worst-case standard deviation was about **0.32% of mean RPM**
- standard deviation was generally around **0.16–0.43 RPM**
- worst-case peak-to-peak variation was about **1.20 RPM**

The very large percentage value near duty 25 was ignored because the motor was essentially stopped there, so dividing by a mean RPM close to zero makes the percentage meaningless.

## Decision

No velocity filter will be added at this stage.

The raw RPM signal is already stable enough at the current 200 ms measurement interval, and adding a filter would introduce extra delay into the feedback signal without solving a significant noise problem.

If the closed-loop controller later uses a much faster measurement interval, RPM noise should be checked again at that new sample rate.