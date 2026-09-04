#include <Arduino.h>

void setup()
{
    pinMode(LED_BUILTIN, OUTPUT);   // onboard LED pin, output mode

    Serial.begin(115200);           // must match monitor_speed in platformio.ini
    delay(500);                     // let the USB-serial link settle before printing

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