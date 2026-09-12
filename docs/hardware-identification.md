# Hardware Identification

**Status:** Hardware mostly confirmed. The 12 V supply has been meter-verified, but 12 V has not yet been applied to the DRV8871 or motor.

## Motor — CONFIRMED

- Model marking: JGA25-370
- Rated voltage: DC 12 V
- Nominal output speed: 150 RPM
- Source: physical label + Amazon listing ASIN B08LD26BBG

| Wire | Function |
|---|---|
| Red | Motor + |
| White | Motor − |
| Blue | Encoder VCC |
| Black | Encoder GND |
| Yellow | Encoder signal 1 |
| Green | Encoder signal 2 |

- Encoder supply range: 3.3–5 V (seller listing)
- Uno 5 V rail is within the stated encoder supply range
- A/B assignment: NOT yet determined
- Yellow and Green will be called signal 1 / signal 2 until their phase relationship is observed

### Encoder Resolution — UNRESOLVED

The seller states "11 signals from the motor."

This wording does not specify:

- pulses vs. counts
- per channel vs. total
- motor shaft vs. output shaft
- rising edges only vs. all quadrature edges

Working hypothesis only:

- 11 PPR per channel may refer to the motor shaft
- x4 quadrature decoding would then produce 44 counts per motor revolution
- gearbox reduction would further multiply counts per output-shaft revolution

This is NOT being treated as confirmed.

Encoder resolution will be established experimentally during Stage 3 by rotating the output shaft a known amount and counting encoder transitions.

---

## DRV8871 Motor Driver — CONFIRMED

Module markings:

- DRV8871
- HW-062 V2.0.1
- Brushed-DC H-bridge motor driver

Board connections:

- `OUT1`, `OUT2` — motor output screw terminal
- `VM`, `GND` — 12 V motor-supply screw terminal
- `IN2`, `IN1`, `VM`, `GND` — 4-pin header

### Connector Installation

Connectors were soldered onto DRV8871 board #3:

- Both 2-position green screw terminals installed
- 4-pin male header installed
- 8 solder joints completed
- No visible solder bridges
- Adjacent-pin continuity checks showed no shorts
- Board has not yet been powered from 12 V

### Important Power Notes

- The `VM` pin on the 4-pin header is electrically the same motor-supply rail as `VM` on the screw terminal
- `VM` is approximately 12 V in this project
- **Do not connect Arduino 5 V to DRV8871 VM**
- The DRV8871 does not require a separate external logic-supply connection
- Arduino and DRV8871 grounds must be connected together

### H-Bridge Logic

IN1 and IN2 jointly select the H-bridge state:

| IN1 | IN2 | Result |
|---|---|---|
| 0 | 0 | Coast / bridge disabled; sleep after approximately 1 ms |
| 1 | 0 | Forward |
| 0 | 1 | Reverse |
| 1 | 1 | Brake |

Planned Arduino connections:

- Arduino D9 -> DRV8871 IN1
- Arduino D10 -> DRV8871 IN2
- Arduino GND -> DRV8871 GND

The DRV8871 header `VM` pin will intentionally remain unconnected.

### Onboard Components

- 47 uF / 50 V electrolytic bulk capacitor
- Ceramic bypass capacitor
- ILIM-setting resistor present

### Current-Limit Resistor — UNRESOLVED

The exact `RILIM` value has not been confirmed.

The small surface-mount resistor appears to be marked approximately:

- `EDE`
- or possibly `E0E`

The marking has not been reliably decoded.

In-circuit resistance measurements were polarity-dependent:

- approximately 21.6 kOhm in one probe direction
- approximately 6.6 kOhm with the probes reversed

Because the resistor remains connected to the DRV8871 circuitry, neither reading is being treated as the isolated resistor value.

No exact current-limit threshold is being claimed until the resistor value or module behavior is verified more reliably.

---

## Motor Power Supply — CONFIRMED

Supply:

- Model: ALT-1202
- Input: 100–240 VAC, 50/60 Hz
- Output rating: 12 V DC, 2 A
- Maximum rated output power: 24 W
- Barrel connector used with female barrel-to-screw-terminal adapter

Verification:

- Barrel adapter `+` and `-` terminals are labeled
- Polarity meter-verified
- Measured unloaded output: **12.61 V DC**
- Reversing the meter probes produced **-12.61 V**
- Supply has not yet been connected to the DRV8871 or motor

Planned connection:

- Adapter positive -> DRV8871 `VM`
- Adapter negative -> DRV8871 `GND`

---

## Controller — CONFIRMED

- Whadda / Velleman WPB100 ATmega328 UNO development board
- Vendor states Arduino Uno compatibility
- Standard D0–D13 / A0–A5 labels confirmed from photos
- PlatformIO board target: `uno`

### Planned Pin Assignment

| Arduino Pin | Function |
|---|---|
| D2 | Encoder signal 1 |
| D3 | Encoder signal 2 |
| D9 | DRV8871 IN1 |
| D10 | DRV8871 IN2 |
| D0 / D1 | Reserved for USB serial |
| D13 | Available for status/debug LED |

D2 and D3 are reserved for encoder interrupt inputs during Stage 3.

D9 and D10 are used for DRV8871 control during Stage 2.

---

## Arduino to DRV8871 Connections

Only three logic connections are required:

| Arduino | DRV8871 |
|---|---|
| D9 | IN1 |
| D10 | IN2 |
| GND | GND |

Shared ground is required so the DRV8871 has the same voltage reference as the Arduino PWM signals.

The DRV8871 header `VM` pin will remain empty.

---

## Stage 2 Firmware Status

Stage 2 open-loop PWM firmware has been:

- written in `src/main.cpp`
- built successfully in PlatformIO
- uploaded successfully to the ATmega328 board
- verified through the Serial Monitor at 115200 baud

Serial controls:

- `0`–`9` = 0–90% duty
- `f` = 100% duty
- `s` = stop
- `d` = flip direction after stopping

The motor has not yet been connected or powered.

---

## Open Items Before First Motor Power-On

- [x] Identify motor voltage and nominal speed
- [x] Identify motor wire functions
- [x] Identify DRV8871 board connections
- [x] Meter-verify 12 V adapter voltage
- [x] Meter-verify adapter polarity
- [x] Solder DRV8871 screw terminals and header
- [x] Check soldered board for obvious shorts
- [x] Select Arduino control pins
- [x] Create Stage 2 wiring table
- [x] Build and upload Stage 2 firmware
- [x] Verify Stage 2 serial interface
- [ ] Secure / brace motor before operation
- [ ] Physically connect Arduino to DRV8871
- [ ] Physically connect motor to DRV8871
- [ ] Physically connect 12 V supply to DRV8871
- [ ] Perform first open-loop motor test

Still unresolved but not currently blocking first motor power-on:

- Exact encoder counts per output-shaft revolution
- Exact DRV8871 `RILIM` value / current-limit thresholdd