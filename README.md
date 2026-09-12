# Closed-Loop DC Motor Speed Control (PI/PID)

Closed-loop speed control of a brushed DC gearmotor using quadrature encoder feedback and a PI/PID controller implemented on an ATmega328.

**Status:** Stage 2 — Open-Loop PWM Bring-Up

Stage 1 hardware identification and development-tool verification are complete.

Stage 2 firmware has been built, uploaded, and verified through the serial interface. The DRV8871 module has been assembled and checked for obvious solder shorts, and the 12 V supply has been meter-verified at 12.61 V unloaded.

The first physical open-loop motor test is pending the remaining logic wiring.

---

## Problem

Commanding a fixed PWM duty cycle does not guarantee a known motor speed.

Motor speed changes with:

- friction
- supply conditions
- mechanical load
- motor characteristics

This project closes the feedback loop by measuring actual motor RPM, comparing it against a commanded RPM, and automatically adjusting the motor PWM command.

The final goal is to demonstrate stable speed regulation, quantify the transient response, and evaluate how well the controller rejects load disturbances.

---

## Hardware

| Part | Role |
|---|---|
| JGA25-370 12 V / 150 RPM gearmotor with quadrature encoder | Motor + velocity feedback |
| DRV8871 H-bridge module | Motor power stage |
| Whadda ATmega328 UNO board | Real-time controller |
| 12 V / 2 A regulated adapter | Motor power supply |
| Digilent Analog Discovery 3 | Oscilloscope / logic analysis |
| AstroAI DM130B multimeter | Electrical measurements |

---

## Current Hardware Status

### Motor

- JGA25-370
- 12 V
- 150 RPM nominal output speed
- Integrated encoder
- Encoder resolution still to be measured experimentally

### DRV8871

- HW-062 V2.0.1 module
- Two screw terminals soldered
- 4-pin header soldered
- 8 joints completed
- No visible solder bridges
- Adjacent-pin continuity checks showed no obvious shorts

### Power Supply

- Rated output: 12 V / 2 A
- Measured unloaded output: **12.61 V DC**
- Polarity meter-verified

### Controller

- Whadda / Velleman ATmega328 UNO-compatible board
- PlatformIO target: `uno`
- Stage 2 firmware builds and uploads successfully
- Serial Monitor verified at 115200 baud

---

## Stage 2 Wiring

### Arduino -> DRV8871

| Arduino | DRV8871 |
|---|---|
| D9 | IN1 |
| D10 | IN2 |
| GND | GND |

The DRV8871 header `VM` pin is intentionally left unconnected.

### 12 V Supply -> DRV8871

| Adapter | DRV8871 |
|---|---|
| + | VM |
| - | GND |

### DRV8871 -> Motor

| DRV8871 | Motor |
|---|---|
| OUT1 | Red |
| OUT2 | White |

Encoder wires remain disconnected during Stage 2.

---

## Stage 2 Control Scheme

Initial open-loop testing uses coast-mode PWM.

Forward:

- IN2 held LOW
- PWM applied to IN1

Reverse:

- IN1 held LOW
- PWM applied to IN2

Serial commands:

| Command | Action |
|---|---|
| `0`–`9` | 0–90% PWM duty |
| `f` | 100% duty |
| `s` | Stop / coast |
| `d` | Stop and flip direction |

Drive-brake PWM may be compared later during open-loop characterization.

---

## Repository Layout

- `platformio.ini` — PlatformIO build configuration
- `src/` — firmware source; one evolving project preserved through Git commits and tags
- `include/`, `lib/`, `test/` — standard PlatformIO directories
- `docs/` — hardware identification, wiring, control theory, tuning, debugging notes
- `data/` — raw experimental CSV logs
- `analysis/` — Python data-analysis and plotting scripts
- `images/` — hardware photos, wiring photos, oscilloscope captures, and plots

---

## Project Progress

- [x] Stage 1 — Hardware identification and toolchain verification
- [ ] Stage 2 — Open-loop PWM motor control
- [ ] Stage 3 — Quadrature encoder bring-up
- [ ] Stage 4 — RPM measurement
- [ ] Stage 5 — Open-loop PWM vs. RPM characterization
- [ ] Stage 6 — Velocity filtering, if justified by measurements
- [ ] Stage 7 — Proportional control
- [ ] Stage 8 — PI control
- [ ] Stage 9 — PID evaluation if derivative action provides measurable benefit
- [ ] Stage 10 — Step-response and disturbance testing
- [ ] Stage 11 — Final plots, quantitative results, documentation, and demo

Stage 2 will be marked complete only after the motor has successfully:

- started under PWM control
- changed speed with duty command
- stopped on command
- rotated in both directions

---

## Planned Experimental Measurements

### Open-Loop Characterization

- Minimum PWM duty that produces motion
- PWM duty vs. measured RPM
- Direction verification
- Motor-supply voltage while running

### Encoder

- Encoder counts per output-shaft revolution
- Signal phase relationship
- RPM calculation accuracy

### Closed-Loop Control

- Commanded RPM
- Measured RPM
- Control error
- PWM command
- Control-loop timing

### Step Response

- Rise time
- Settling time
- Peak overshoot
- Steady-state error

### Disturbance Response

- Initial speed drop
- Controller response
- Recovery time
- Final steady-state error

---

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

---

## References

- Texas Instruments DRV8871 datasheet
- Motor manufacturer / seller specifications
- DRV8871 module product documentation