#include <Arduino.h>

void setup()
{
    pinMode(LED_BUILTIN, OUTPUT);

    Serial.begin(115200);
    delay(500);

    Serial.println("DC Motor PID Control Project");
    Serial.println("Stage 1: PlatformIO firmware test");
}

void loop()
{
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.println("LED ON");
    delay(500);

    digitalWrite(LED_BUILTIN, LOW);
    Serial.println("LED OFF");
    delay(500);
}