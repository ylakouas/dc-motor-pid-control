# Wiring — Stage 2 (open-loop motor)

Status: not yet physically connected. Awaiting male-to-female jumper wires.

## Arduino -> DRV8871 (logic)
| Arduino | DRV8871 |
|---|---|
| D9  | IN1 |
| D10 | IN2 |
| GND | GND (header) |

## 12 V supply -> DRV8871 (power screw terminal)
| Adapter | DRV8871 |
|---|---|
| + | VM |
| - | GND |

Adapter polarity meter-verified: yes.
Measured 12.61 V DC unloaded; -12.61 V with probes reversed.

## DRV8871 -> Motor (motor screw terminal)
| DRV8871 | Motor |
|---|---|
| OUT1 | Red |
| OUT2 | White |

## Not connected at this stage
- DRV8871 header VM pin: intentionally empty. Same net as the 12 V
  screw terminal. Arduino 5 V here would destroy the board.
- Encoder (Blue/Black/Yellow/Green): Stage 3. Ends taped off.

## Control scheme
Coast-mode PWM. IN2 low, PWM on IN1 for forward; reversed for reverse.
Drive-brake mode to be compared during Stage 5 characterization.

## Measurements to record during first power-up
- [ ] Adapter voltage unloaded: 12.61 V
- [ ] VM at screw terminal, motor running: ____
- [ ] Lowest duty command producing motion (deadband): ____
- [ ] Both directions confirmed: ____
- [ ] DRV8871 chip temperature impression after 100% run: ____