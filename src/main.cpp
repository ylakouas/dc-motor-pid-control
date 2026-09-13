#include <Arduino.h>

// motor driver (Stage 2)
const int IN1 = 9;
const int IN2 = 10;

int duty = 0;
bool forward = true;

// encoder (Stage 3)
const int ENC_A = 2;   // Yellow, INT0
const int ENC_B = 3;   // Green, INT1

volatile long encoderCount = 0;
volatile uint8_t lastEncoded = 0;

// RPM calculation (Stage 4)
const float COUNTS_PER_REV = 2500.0;  // measured, x4 decode, output shaft
long lastCount = 0;

unsigned long lastPrintTime = 0;
const unsigned long PRINT_INTERVAL_MS = 200;

void coast()
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

    if (forward) {
        digitalWrite(IN2, LOW);
        analogWrite(IN1, duty);
    } else {
        digitalWrite(IN1, LOW);
        analogWrite(IN2, duty);
    }
}

void updateEncoder()
{
    int a = digitalRead(ENC_A);
    int b = digitalRead(ENC_B);
    uint8_t encoded = (a << 1) | b;
    uint8_t transition = (lastEncoded << 2) | encoded;

    switch (transition) {
        case 0b0001: case 0b0111: case 0b1110: case 0b1000:
            encoderCount++;
            break;
        case 0b0010: case 0b1011: case 0b1101: case 0b0100:
            encoderCount--;
            break;
    }

    lastEncoded = encoded;
}

void setup()
{
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    coast();

    pinMode(ENC_A, INPUT);
    pinMode(ENC_B, INPUT);
    lastEncoded = (digitalRead(ENC_A) << 1) | digitalRead(ENC_B);
    attachInterrupt(digitalPinToInterrupt(ENC_A), updateEncoder, CHANGE);
    attachInterrupt(digitalPinToInterrupt(ENC_B), updateEncoder, CHANGE);

    Serial.begin(115200);
    delay(500);
    Serial.println("millis,duty,count,rpm");  // CSV header, once per boot
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
            duty = 0;
            coast();
            forward = !forward;
        }

        drive();
    }

    unsigned long now = millis();
    if (now - lastPrintTime >= PRINT_INTERVAL_MS) {
        lastPrintTime = now;

        noInterrupts();
        long countSnapshot = encoderCount;
        interrupts();

        long deltaCount = countSnapshot - lastCount;
        lastCount = countSnapshot;

        float rpm = (deltaCount / COUNTS_PER_REV) * (60000.0 / PRINT_INTERVAL_MS);

        Serial.print(now);
        Serial.print(",");
        Serial.print(duty);
        Serial.print(",");
        Serial.print(countSnapshot);
        Serial.print(",");
        Serial.println(rpm, 2);
    }
}