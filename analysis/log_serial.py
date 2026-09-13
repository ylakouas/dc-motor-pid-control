"""
Logs Arduino serial output to a CSV file while allowing commands
to be sent from this same terminal.

Usage:
    python3 analysis/log_serial.py data/stage5_pwm_sweep.csv
"""

import serial
import sys
import threading

PORT = "/dev/cu.usbmodem11101"
BAUD = 115200

if len(sys.argv) < 2:
    print("Usage: python3 analysis/log_serial.py <output_filename.csv>")
    sys.exit(1)

outfile = sys.argv[1]

ser = serial.Serial(PORT, BAUD, timeout=1)
log_file = open(outfile, "w")


def read_serial():
    while True:
        try:
            line = ser.readline().decode("utf-8", errors="ignore").strip()

            if line:
                print(line)
                log_file.write(line + "\n")
                log_file.flush()

        except serial.SerialException:
            break


reader = threading.Thread(target=read_serial, daemon=True)
reader.start()

print(f"Logging {PORT} -> {outfile}")
print("Type motor commands here: 0-9, f, s, d")
print("Type q to stop logging.")

try:
    while True:
        command = input().strip()

        if command.lower() == "q":
            break

        if command in "0123456789fsd" and len(command) == 1:
            ser.write(command.encode("utf-8"))
        else:
            print("Valid commands: 0-9, f, s, d, q")

finally:
    ser.close()
    log_file.close()
    print("Logger stopped.")