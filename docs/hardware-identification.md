# Hardware Identification

**Status:** Core hardware has been identified, wired, and tested. The motor, encoder, DRV8871 driver, Arduino, and 12 V power supply are all working correctly for open-loop speed control and RPM measurement.

## Motor — CONFIRMED

- Model: JGA25-370
- Rated voltage: 12 V DC
- Rated output speed: 150 RPM
- Source: physical motor label and Amazon listing

### Motor wiring

| Wire | Function |
|---|---|
| Red | Motor + |
| White | Motor - |
| Blue | Encoder VCC |
| Black | Encoder GND |
| Yellow | Encoder channel A |
| Green | Encoder channel B |

- Encoder supply range: 3.3–5 V
- Encoder is powered from the Arduino 5 V rail
- Yellow is connected to Arduino D2
- Green is connected to Arduino D3
- Oscilloscope testing showed clean quadrature signals from about 0 V to 5 V
- No external pull-up resistors were needed
- Green led Yellow during the tested default motor direction
- Default motor direction produces increasing encoder counts

### Encoder resolution — RESOLVED

Encoder resolution was measured experimentally using physical output-shaft revolutions and x4 quadrature decoding.

Two clean 20-revolution tests were recorded:

- 49,920 counts / 20 rev = 2496.0 counts/rev
- 50,038 counts / 20 rev = 2501.9 counts/rev

The firmware uses:

**2500 counts per output-shaft revolution**

The two tests differed by about 0.24%. The small difference is likely caused by reaction time and a small amount of motor coasting when starting and stopping the test.

The result is also consistent with the earlier estimate of about 44 x4 counts per motor revolution and a gearbox ratio near 57:1, but this is only a rough consistency check and not a confirmed manufacturer specification.

---

## DRV8871 Motor Driver — CONFIRMED

Module markings:

- DRV8871
- HW-062 V2.0.1
- Brushed DC H-bridge motor driver

### Board connections

- `OUT1`, `OUT2` — motor outputs
- `VM`, `GND` — 12 V motor power input
- `IN2`, `IN1`, `VM`, `GND` — control header

### Current driver board

The currently installed DRV8871 replacement board has:

- Both green screw terminals installed
- 4-pin male header installed
- No visible solder bridges
- 12 V power successfully applied
- Forward and reverse output verified before connecting the motor

Measured with about 12.62 V supplied:

- Forward full duty:
  - OUT1 ≈ 12.61 V
  - OUT2 ≈ 0 V

- Reverse full duty:
  - OUT1 ≈ 0 V
  - OUT2 ≈ 12.61 V

The replacement driver successfully runs the motor in both directions.

A previous DRV8871 board stopped producing valid output and was removed from the project.

### Important power notes

- The `VM` pin on the 4-pin header is electrically connected to the same motor-supply rail as the screw-terminal `VM`
- `VM` is approximately 12 V in this project
- **Arduino 5 V must not be connected to DRV8871 VM**
- Arduino and DRV8871 grounds must be connected together
- The DRV8871 header `VM` pin is intentionally left unused

### H-bridge logic

| IN1 | IN2 | Result |
|---|---|---|
| 0 | 0 | Coast |
| 1 | 0 | Forward |
| 0 | 1 | Reverse |
| 1 | 1 | Brake |

Current Arduino connections:

- Arduino D9 → DRV8871 IN1
- Arduino D10 → DRV8871 IN2
- Arduino GND → DRV8871 GND

### Onboard components

- 47 µF / 50 V electrolytic capacitor
- Ceramic bypass capacitor
- Current-limit resistor

### Current-limit resistor — UNRESOLVED

The exact `RILIM` resistance has not been confirmed.

The small surface-mount resistor appears to be marked approximately:

- `EDE`
- or possibly `E0E`

In-circuit resistance measurements were inconsistent because the resistor is still connected to the rest of the driver circuitry.

Measured values included:

- approximately 21.6 kΩ in one direction
- approximately 6.6 kΩ in the opposite direction

Because of this, neither value is being treated as the actual resistor value.

The exact current-limit setting is still unknown, but this has not prevented successful motor operation.

---

## Motor Power Supply — CONFIRMED

Supply:

- Model: ALT-1202
- Input: 100–240 VAC, 50/60 Hz
- Output: 12 V DC
- Current rating: 2 A
- Maximum power: 24 W

The supply is used with a female barrel-to-screw-terminal adapter.

### Measurements

- Unloaded output: **12.61 V**
- Reverse meter polarity: **-12.61 V**
- DRV8871 VM at idle: **12.61 V**
- DRV8871 VM while motor ran at command `5`: **12.58 V**

The small drop from 12.61 V to 12.58 V shows very little supply voltage sag during this test.

### Current connection

- Adapter positive → DRV8871 `VM`
- Adapter negative → DRV8871 `GND`

---

## Controller — CONFIRMED

- Whadda / Velleman WPB100 ATmega328 UNO board
- Arduino Uno compatible
- PlatformIO board target: `uno`
- Serial baud rate: 115200

### Current pin assignment

| Arduino Pin | Function |
|---|---|
| D2 | Encoder A — Yellow |
| D3 | Encoder B — Green |
| D9 | DRV8871 IN1 |
| D10 | DRV8871 IN2 |
| D0 / D1 | USB serial |
| D13 | Available for status/debug LED |

D2 and D3 are used as interrupt inputs for x4 quadrature decoding.

D9 and D10 control the DRV8871 for PWM speed control and direction.

---

## Arduino to DRV8871 Connections

| Arduino | DRV8871 |
|---|---|
| D9 | IN1 |
| D10 | IN2 |
| GND | GND |

The DRV8871 header `VM` pin remains empty.

A shared ground is required so the Arduino PWM signals and the motor driver use the same voltage reference.

---

## Encoder Connections

| Encoder Wire | Arduino |
|---|---|
| Blue | 5 V |
| Black | GND |
| Yellow | D2 |
| Green | D3 |

The encoder was also checked with the Analog Discovery 3 before being connected to D2 and D3.

Measured encoder signal characteristics:

- approximately 0–5 V
- clean square-wave output
- quadrature phase offset between channels
- about 50% duty cycle on the encoder signal
- no external pull-ups required

---

## Firmware and Test Status

The current firmware supports:

- Serial motor commands
- Open-loop PWM speed control
- Direction reversal
- x4 quadrature encoder decoding
- Signed encoder counting
- RPM measurement
- CSV serial logging

### Motor test results

- Motor starts and runs at command `2`
- Commands `2`, `3`, `4`, and `5` produced increasing speed
- `s` stops the motor
- `d` reverses direction
- `f` successfully ran the motor at full speed

Full-speed testing showed:

- no grinding
- no burning smell
- no smoke
- stable motor fixture
- driver remained cool

### RPM measurements

- Idle: **0.0 RPM**
- Full duty `f`: approximately **149–150 RPM**
- Command `5`: approximately **124 RPM**
- Reverse command `2`: approximately **-55 RPM**

The full-speed result closely matches the motor's 150 RPM rating.

---

## Open-Loop Characterization

A full PWM sweep was completed from duty 0 to 255 and back down to 0.

Raw data:

`data/stage5_pwm_sweep.csv`

Serial logger:

`analysis/log_serial.py`

Analysis script:

`analysis/analyze_stage5.py`

Plot:

`images/stage5_pwm_vs_rpm.png`

Main observations:

- Motor is stopped at duty 25
- Motor is running by duty 51
- Startup threshold is somewhere between those values
- Speed response is strongly nonlinear
- Around 50% PWM already produces about 82% of maximum speed
- The speed curve begins flattening strongly at higher duty values
- A small difference exists between ascending and descending speed measurements

More detail is documented in:

`docs/stage5-characterization.md`

---

## Remaining Hardware Uncertainty

The main unresolved hardware detail is the exact DRV8871 current-limit setting.

The onboard `RILIM` resistor has not been identified accurately enough to calculate the exact current limit.

This has not caused any problems during open-loop motor testing or characterization.