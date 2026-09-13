# Stage 5 — PWM vs RPM Characterization

## Method

A full-range open-loop PWM sweep was performed from duty 0 to 255 and
then back down to 0. Each duty command was held for approximately 4 s.

Motor speed was logged using `analysis/log_serial.py` to:

`data/stage5_pwm_sweep.csv`

Settled RPM was calculated with `analysis/analyze_stage5.py` by taking
the median RPM from the back half of each constant-duty segment. This
reduces the influence of transient acceleration or deceleration after
each command change.

## Settled RPM

| Duty | RPM (up) | RPM (down) | Hysteresis | Hysteresis % |
|---|---:|---:|---:|---:|
| 0   | 0.00   | 0.00   | -     | -     |
| 25  | 0.00   | 0.00   | -     | -     |
| 51  | 51.72  | 56.16  | +4.44 | 8.6%  |
| 76  | 89.46  | 93.48  | +4.02 | 4.5%  |
| 102 | 110.76 | 113.52 | +2.76 | 2.5%  |
| 127 | 123.36 | 125.28 | +1.92 | 1.6%  |
| 153 | 132.72 | 134.04 | +1.32 | 1.0%  |
| 178 | 137.76 | 138.60 | +0.84 | 0.6%  |
| 204 | 141.48 | 141.96 | +0.48 | 0.3%  |
| 229 | 144.24 | 144.48 | +0.24 | 0.17% |
| 255 | 149.88 | 149.88 | -     | -     |

Plot:

`images/stage5_pwm_vs_rpm.png`

## Startup deadband

The motor remained stopped at duty 25 (~10% PWM) and was rotating at
51.72 RPM by duty 51 (~20% PWM) during the ascending sweep.

Therefore, the startup threshold lies somewhere between duty 25 and 51.
The exact threshold was not resolved because intermediate duty values
were not tested during this sweep.

This deadband will be important during closed-loop control because the
controller must produce enough drive to overcome the motor and gearbox
startup friction before rotation begins.

## Nonlinearity

The open-loop duty-to-speed relationship is strongly nonlinear.

Approximately 50% PWM (duty 127) produced 123.36 RPM, which is about
82% of the measured full-speed value of 149.88 RPM.

The measured incremental gain decreased substantially as duty increased:

- duty 25→51: ~1.99 RPM per duty count
- duty 51→76: ~1.51
- duty 76→102: ~0.82
- duty 102→127: ~0.50
- duty 127→153: ~0.36
- duty 153→178: ~0.20
- duty 178→204: ~0.14
- duty 204→229: ~0.11

This means a fixed controller gain may behave differently across the
motor's operating range.

## Hysteresis

Descending RPM was consistently slightly higher than ascending RPM at
the same PWM command.

The difference was largest at low duty:

- duty 51: +4.44 RPM
- duty 76: +4.02 RPM
- duty 102: +2.76 RPM

The difference decreased steadily as duty increased and was only
+0.24 RPM by duty 229.

This behavior is consistent with effects such as static versus kinetic
friction in the motor/gearbox system, although this experiment alone
does not isolate the exact physical cause.

## High-duty flattening

The speed curve begins flattening strongly above roughly duty 150–180.
Increasing PWM beyond this region produces progressively smaller speed
increases as the motor approaches its unloaded maximum speed.

Measured maximum speed at duty 255 was 149.88 RPM, closely matching the
150 RPM motor nameplate.

## Drive scheme

This characterization used coast-mode PWM:

- one DRV8871 input held LOW
- PWM applied to the other input

Drive-brake PWM was not characterized.

Coast mode produced a smooth, monotonic speed curve and is sufficient
for proceeding to closed-loop testing. Drive-brake mode can be
evaluated later if closed-loop testing shows a need for stronger
deceleration behavior.