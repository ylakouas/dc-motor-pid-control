#include <Arduino.h>

// motor driver
const int IN1 = 9;
const int IN2 = 10;

// encoder
const int ENC_A = 2;
const int ENC_B = 3;

volatile long encoderCount = 0;
volatile uint8_t lastEncoded = 0;

// RPM / control timing
const float COUNTS_PER_REV = 2500.0;
long lastCount = 0;

unsigned long lastControlTime = 0;
const unsigned long CONTROL_INTERVAL_MS = 200;

// P controller
float Kp = 0.4;
int targetRpm = 0;
bool controllerEnabled = false;

// non-blocking serial input
const int SERIAL_BUF_SIZE = 16;
char serialBuf[SERIAL_BUF_SIZE];
int serialBufIndex = 0;

void coast()
{
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
}

void driveSigned(int output)
{
    if (output == 0) {
        coast();
    } else if (output > 0) {
        digitalWrite(IN2, LOW);
        analogWrite(IN1, output);
    } else {
        digitalWrite(IN1, LOW);
        analogWrite(IN2, -output);
    }
}

int clampOutput(int output)
{
    if (output > 255) return 255;
    if (output < -255) return -255;
    return output;
}

void updateEncoder()
{
    int a = digitalRead(ENC_A);
    int b = digitalRead(ENC_B);

    uint8_t encoded = (a << 1) | b;
    uint8_t transition = (lastEncoded << 2) | encoded;

    switch (transition) {
        case 0b0001:
        case 0b0111:
        case 0b1110:
        case 0b1000:
            encoderCount++;
            break;

        case 0b0010:
        case 0b1011:
        case 0b1101:
        case 0b0100:
            encoderCount--;
            break;
    }

    lastEncoded = encoded;
}

void processCommand(char *cmd)
{
    if (cmd[0] == 's' || cmd[0] == 'S') {
        controllerEnabled = false;
        targetRpm = 0;
        coast();
    } else {
        targetRpm = atoi(cmd);
        controllerEnabled = true;
    }
}

void checkSerial()
{
    while (Serial.available()) {
        char c = Serial.read();

        if (c == '\n' || c == '\r') {
            if (serialBufIndex > 0) {
                serialBuf[serialBufIndex] = '\0';
                processCommand(serialBuf);
                serialBufIndex = 0;
            }
        } else if (serialBufIndex < SERIAL_BUF_SIZE - 1) {
            serialBuf[serialBufIndex++] = c;
        }
    }
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

    Serial.println("millis,target_rpm,rpm,error,output");
}

void loop()
{
    checkSerial();

    unsigned long now = millis();

    if (now - lastControlTime >= CONTROL_INTERVAL_MS) {
        lastControlTime = now;

        noInterrupts();
        long countSnapshot = encoderCount;
        interrupts();

        long deltaCount = countSnapshot - lastCount;
        lastCount = countSnapshot;

        float rpm =
            (deltaCount / COUNTS_PER_REV) *
            (60000.0 / CONTROL_INTERVAL_MS);

        float error = targetRpm - rpm;
        int output = 0;

        if (controllerEnabled) {
            output = clampOutput((int)(Kp * error));
            driveSigned(output);
        } else {
            coast();
        }

        Serial.print(now);
        Serial.print(",");
        Serial.print(targetRpm);
        Serial.print(",");
        Serial.print(rpm, 2);
        Serial.print(",");
        Serial.print(error, 2);
        Serial.print(",");
        Serial.println(output);
    }
}