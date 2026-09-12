# Hardware Identification

Status: mostly confirmed. No 12 V has been applied yet.

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

- Encoder supply range: 3.3–5 V (listing). Uno 5 V rail is in range.
- A/B assignment: NOT yet determined. Yellow/Green called signal 1 / signal 2
  until phase relationship is observed on the scope.

### Encoder resolution — UNRESOLVED

Seller states "11 signals from the motor." Wording does not specify
pulses vs counts, per channel or total, or motor shaft vs output shaft.

Working hypothesis (unverified): 11 PPR per channel on the motor shaft,
x4 quadrature = 44 counts per motor rev, x gear ratio = counts per
output rev.

To be established experimentally in Stage 3 by hand-turning the output
shaft a known number of revolutions and counting edges.

## DRV8871 module — CONFIRMED

Screw terminals (2 x 2-position, not yet soldered):
- OUT1, OUT2 — motor
- VM, GND — 12 V motor supply

4-pin header (not yet soldered):
- IN2, IN1, VM, GND

**VM on the header is the same net as VM on the screw terminal. It is the
12 V motor rail, NOT a logic supply. Never connect Arduino 5 V to it.**

The DRV8871 needs no logic supply; IN1/IN2 accept up to 5.5 V logic directly.
IN1 controls OUT1, IN2 controls OUT2.

- Onboard capacitor: 47 uF / 50 V electrolytic, polarized.
  Reversed supply polarity will reverse-bias it. Verify polarity first.
- Current limit (ILIM): TBD. Not broken out on the header. Check for an
  SMD resistor near the chip. I_trip ~= 66500 / R_ILIM (verify vs TI datasheet).
  - Connectors: SOLDERED. Both 2-position screw terminals and the 4-pin header installed on board #3. 8 joints, no visible bridges. Continuity check across adjacent pins: no continuity. Unpowered.

## Power supply — CONFIRMED

- Model: ALT-1202
- Output: DC 12 V / 2 A / 24 W
- Barrel polarity: center-positive, meter-verified.
- Measured output voltage: 12.61 V DC unloaded (-12.61 V probes reversed).

## Controller — CONFIRMED

- Whadda / Velleman WPB100 ATmega328 UNO development board
- Vendor states 100% Arduino Uno compatible
- Standard D0-D13 / A0-A5 labels confirmed from photos
- PlatformIO: board = uno

## Connections between Arduino and DRV8871

Only three: IN1, IN2, and GND. Shared ground is required so the driver
has a reference for the PWM signal.

## Open items before power-on

- [ ] Meter-verify 12 V adapter polarity and voltage
- [ ] Identify ILIM resistor on DRV8871
- [ ] Solder DRV8871 connectors
- [ ] Final Arduino pin assignments
- [ ] Reviewed pin-to-pin wiring table