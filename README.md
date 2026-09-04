# Closed-Loop DC Motor Speed Control (PI/PID)

Closed-loop speed control of a brushed DC gearmotor using quadrature
encoder feedback and a PI/PID controller implemented on an ATmega328.

**Status:** Stage 1 — Hardware Identification

## Problem

Commanding a fixed PWM duty cycle does not guarantee a known motor
speed. Motor speed changes with friction, supply conditions, and
mechanical load.

This project closes the feedback loop by measuring actual motor RPM,
comparing it against a commanded RPM, and automatically adjusting the
motor PWM command.

## Hardware

| Part | Role |
|---|---|
| GA25-370 12 V gearmotor with A/B encoder | Motor + velocity feedback |
| DRV8871 H-bridge module | Motor power stage |
| Whadda ATmega328 UNO board | Real-time controller |
| 12 V / 2 A regulated adapter | Motor power supply |
| Digilent Analog Discovery 3 | Oscilloscope / logic analysis |
| AstroAI DM130B multimeter | Electrical measurements |

## Repository Layout

- `docs/` — hardware identification, wiring, control theory, tuning, and debugging
- `firmware/` — PlatformIO embedded firmware project
- `data/` — raw experimental CSV logs
- `analysis/` — Python data-analysis and plotting scripts
- `images/` — hardware photos, wiring photos, and oscilloscope captures

## Build Stages

- [ ] 1. Hardware identification and wiring table
- [ ] 2. Open-loop PWM motor control
- [ ] 3. Quadrature encoder bring-up
- [ ] 4. RPM measurement
- [ ] 5. Open-loop PWM vs. RPM characterization
- [ ] 6. Velocity filtering, if justified by measurements
- [ ] 7. Proportional control
- [ ] 8. PI control
- [ ] 9. PID evaluation
- [ ] 10. Step-response and disturbance testing

## Final Measurements

| Metric | Value |
|---|---|
| Encoder counts per output-shaft revolution | TBD |
| Control-loop rate | TBD |
| Commanded speed | TBD |
| Measured steady-state speed | TBD |
| Steady-state error | TBD |
| Rise time | TBD |
| Settling time | TBD |
| Peak overshoot | TBD |
| Disturbance speed drop | TBD |
| Disturbance recovery time | TBD |

## References

- Texas Instruments DRV8871 datasheet
- Motor manufacturer / seller specifications