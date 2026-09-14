# Final Closed-Loop Characterization

## Final Controller

The final motor-speed controller uses proportional-integral feedback.

Controller settings:

- Kp = 0.40
- Ki = 0.30
- Control interval = 200 ms
- Encoder resolution = 2500 counts/output revolution
- Output range = -255 to +255
- Velocity filtering = none

Conditional-integration anti-windup prevents the integral term from
continuing to grow when controller output saturation would otherwise occur.

The final tests did not require output saturation.

## P vs PI Control

Stage 7 used proportional-only control with Kp = 0.4.

At a +130 RPM target, P-only control settled near +30 RPM.
At a -130 RPM target, it settled near -29 RPM.

This produced approximately 100 RPM of steady-state error because the
controller required a persistent error to generate enough PWM to maintain
motor speed.

Adding integral control greatly reduced the steady-state error.

At the final +130 RPM test, measured speed averaged approximately
129.4 RPM near steady state, giving less than 1 RPM of steady-state error.

## Step-Response Results

| Test | 10-90% Rise/Fall Time | 2% Settling Time | Overshoot | Final Speed |
| --- | ---: | ---: | ---: | ---: |
| 0 to +60 RPM | ~5.4 s | ~10.8 s | ~1.6% | ~60.07 RPM |
| 0 to +130 RPM | ~8.8 s | ~22.8 s | 0% | ~129.42 RPM |
| +130 to +90 RPM | ~11.8 s | ~15.8 s | minimal | ~90.53 RPM |
| 0 to -130 RPM | ~8.4 s | ~22.6 s | 0% | ~-128.62 RPM |

The controller remained stable during each tested setpoint change.

The 60 RPM response showed a small amount of overshoot, while the
130 RPM forward and reverse responses approached the setpoint without
significant overshoot.

## Disturbance Test

The motor was operated at a 100 RPM setpoint and an external mechanical
load was briefly applied to the output shaft.

Before the disturbance, speed was approximately 99-100 RPM.

During the clearest loaded portion, speed fell to approximately:

94.56 RPM

This corresponds to roughly a 5.3% speed reduction.

The controller output increased from approximately 80-81 PWM counts to
approximately 85-86 PWM counts in response to the increased error.

After the load was removed, motor speed increased through the setpoint
and briefly reached approximately 104.4 RPM before trending back toward
100 RPM.

Because the applied load was manual and the test was stopped before a
full post-disturbance settling period was recorded, an exact disturbance
recovery settling time is not reported.

The test still demonstrates the expected closed-loop response:
additional mechanical load causes the PI controller to increase motor
drive in an attempt to restore the commanded speed.

## PID Decision

A derivative term was not added to the final controller.

The tuned PI controller showed stable behavior, small steady-state error,
little overshoot, and no sustained oscillation.

The measured RPM signal also contains small quantization and measurement
noise. A derivative term would increase sensitivity to this noise without
addressing a clear problem observed in the final PI response.

PI control was therefore selected as the final architecture.

## Final Result

The project successfully progressed from open-loop PWM control to
encoder-based closed-loop bidirectional motor-speed control.

Experimental characterization included:

- quadrature encoder verification
- encoder resolution measurement
- open-loop PWM versus RPM characterization
- RPM noise analysis
- P-only closed-loop control
- PI tuning
- forward and reverse step-response testing
- steady-state error measurement
- disturbance testing

The final PI controller tracks commanded speed in both directions and
reduces the large steady-state error observed with proportional-only
control.

## Data

- `data/final_characterization.csv`
- `data/final_disturbance.csv`

## Plots

- `images/final_step_response.png`
- `images/final_disturbance_response.png`