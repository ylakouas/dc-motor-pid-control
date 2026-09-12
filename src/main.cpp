#include <Arduino.h>

const int IN1 = 9;    // DRV8871 IN1
const int IN2 = 10;   // DRV8871 IN2

int duty = 0;         // 0-255
bool forward = true;

void coast()          // both low = bridge off
{
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
}

void drive()
{
    if (duty == 0) {
        coast();
        return;
    }

    // coast-mode PWM: one pin PWMs, the other stays low
    if (forward) {
        digitalWrite(IN2, LOW);
        analogWrite(IN1, duty);
    } else {
        digitalWrite(IN1, LOW);
        analogWrite(IN2, duty);
    }
}

void setup()
{
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    coast();            // safe state before 12V goes on

    Serial.begin(115200);
    delay(500);
    Serial.println("Stage 2: open-loop PWM");
    Serial.println("0-9 = 0-90% duty, f = 100%, s = stop, d = flip direction");
}

void loop()
{
    if (Serial.available()) {
        char c = Serial.read();

        if (c >= '0' && c <= '9') {
            duty = (c - '0') * 255 / 10;
        } else if (c == 'f') {
            duty = 255;
        } else if (c == 's') {
            duty = 0;
        } else if (c == 'd') {
            duty = 0;         // always stop before reversing
            coast();
            forward = !forward;
        }

        drive();

        Serial.print("duty ");
        Serial.print(duty);
        Serial.print("  dir ");
        Serial.println(forward ? "fwd" : "rev");
    }
}