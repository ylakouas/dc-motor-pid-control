# Stage 8 — PI Speed Control

## Goal

Add integral control to the proportional speed controller to reduce the large steady-state error observed during Stage 7.

The controller uses:

error = target RPM - measured RPM

output = Kp * error + Ki * integral(error dt)

## Final Controller Settings

- Kp = 0.4
- Ki = 0.30
- Control interval = 200 ms
- Encoder resolution = 2500 counts/output revolution
- Output range = -255 to +255
- Velocity filtering = none

Conditional-integration anti-windup prevents the integral term from continuing to grow when the controller is saturated and the error would push it farther into saturation.

The stop command disables control, resets the integral term, and coasts the motor.

## Initial PI Test

The first PI test used:

- Kp = 0.4
- Ki = 0.15

Integral action substantially improved tracking compared with P-only control, but convergence was slow.

Ki was increased to 0.30 while Kp remained unchanged.

## Tuned PI Results

At a +60 RPM target, the motor converged to approximately 60 RPM with very small steady-state error.

At a +130 RPM target, speed reached approximately 125–126 RPM during the test interval and continued converging toward the target.

A setpoint change from +130 RPM to +90 RPM produced a smooth decrease in speed without sustained oscillation.

At a -130 RPM target, the motor reached approximately -124 to -125 RPM and continued converging toward the target.

No output saturation was observed during these tests.

The controller remained stable in both directions.

## Comparison with P Control

Stage 7 P-only control at Kp = 0.4 produced approximately:

- +130 RPM target -> +30 RPM measured
- -130 RPM target -> -29 RPM measured

After adding integral control:

- +60 RPM target -> approximately +60 RPM
- +130 RPM target -> approximately +126 RPM during the test
- -130 RPM target -> approximately -125 RPM during the test

The integral term supplies the sustained PWM command required by the motor while the proportional term becomes small as the measured speed approaches the target.

## PID Decision

The PI response is stable and does not show significant overshoot or sustained oscillation.

Because the existing encoder RPM measurement already contains small quantization/noise and the PI controller is stable, a derivative term is not currently justified. Adding derivative action would add sensitivity to measurement noise without addressing an observed control problem.

PI will therefore be used for final characterization unless later testing reveals a specific need for derivative action.

## Data

Initial PI test:

`data/stage8_pi_test.csv`

Tuned PI test:

`data/stage8_pi_tuned.csv`