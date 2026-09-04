# Hardware Identification

## Motor

- Model marking on motor/gearbox: JGA25-370
- Motor type: Brushed DC gearmotor with two-channel encoder
- Rated motor voltage: 12 V DC
- Rated output speed: 150 RPM
- Gear ratio: TBD
- Motor positive wire color: Red
- Motor negative wire color: White
- Encoder supply wire color: Blue
- Encoder ground wire color: Black
- Encoder signal 1 wire color: Yellow
- Encoder signal 2 wire color: Green
- Encoder supply voltage: 3.3-5 V
- Encoder resolution: Seller states "11 signals from the motor"; exact PPR/CPR TBD experimentally
- Resolution specified at motor shaft or output shaft: Not clearly specified
- Specification source: Amazon listing, ASIN B08LD26BBG

### Encoder Notes

The seller identifies Yellow and Green as the two signal-feedback wires
but does not explicitly designate which is channel A versus B.

The seller's phrase "11 signals from the motor" is ambiguous and will
not be treated as a verified counts-per-revolution value.

Effective encoder counts per gearbox output-shaft revolution will be
verified experimentally before final RPM calculations are used.

## DRV8871 Module

- Board/module marking: DRV8871
- Motor supply positive terminal: VM
- Ground terminal: GND
- Motor output terminals: OUT1, OUT2
- Logic/control inputs: IN1, IN2
- Onboard bulk capacitor: 47 uF, 50 V
- Headers already soldered: No
- Screw terminals already soldered: No
- Included connectors: Two 2-position screw terminals and one 4-pin male header
- Current-limit configuration: TBD

### DRV8871 Notes

VM is the motor-supply input, not a 5 V logic-supply input.

The intended motor supply is approximately 12 V.

The ATmega328 and DRV8871 will require a common ground when the final
wiring is assembled.

## Power Supply

- Model: ALT-1202
- Rated input: AC 100-240 V, 50/60 Hz
- Rated output voltage: 12 V DC
- Rated output current: 2 A
- Rated output power: 24 W
- Barrel polarity: Appears center-positive from label; verify with multimeter
- Measured output voltage: TBD

## Barrel Adapter

- Wall-adapter connector: Male barrel plug
- Project adapter: Female barrel socket to screw-terminal adapter
- Terminal polarity: Verify before connection

## Controller

- Board: Velleman / Whadda ATmega328 UNO Development Board
- Microcontroller family: ATmega328
- Standard UNO D0-D13 labels confirmed: Yes
- Standard UNO A0-A5 labels confirmed: Yes
- USB connector: USB-B
- PlatformIO board target: uno
- Voltage jumper/switch present: TBD / verify if applicable

## Open Questions

- Exact encoder counts per revolution
- Exact interpretation of seller's "11 signals from the motor"
- Encoder A/B channel naming
- Gear ratio
- DRV8871 current-limit configuration
- Final ATmega pin assignments
- Final pin-to-pin wiring table
- Measured 12 V adapter output and polarity