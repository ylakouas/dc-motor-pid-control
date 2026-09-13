# Stage 7 — Proportional Speed Control

## Goal

Implement the first closed-loop motor speed controller using proportional feedback.

The controller uses:

```text
error = target RPM - measured RPM
output = Kp * error