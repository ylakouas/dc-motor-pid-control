"""
Interactive serial logger for closed-loop control stages.

Type a target RPM such as:
    130
    80
    -80

Other commands:
    s = stop/coast
    q = quit logger

Usage:
    python3 analysis/log_serial.py data/stage7_p_control_test.csv
"""

import serial
import sys
import threading

PORT = "/dev/cu.usbmodem1101"
BAUD = 115200

if len(sys.argv) < 2:
    print("Usage: python3 analysis/log_serial.py <output_filename.csv>")
    sys.exit(1)

outfile = sys.argv[1]

stop_flag = threading.Event()


def reader_thread(ser, log_file):
    while not stop_flag.is_set():
        try:
            line = ser.readline().decode("utf-8", errors="ignore").strip()
        except serial.SerialException:
            break

        if line:
            print(line)
            log_file.write(line + "\n")
            log_file.flush()


with serial.Serial(PORT, BAUD, timeout=1) as ser, open(outfile, "w") as log_file:
    print(f"Logging {PORT} -> {outfile}")
    print("Enter target RPM, 's' to stop/coast, or 'q' to quit.")

    reader = threading.Thread(
        target=reader_thread,
        args=(ser, log_file),
        daemon=True,
    )
    reader.start()

    try:
        while True:
            command = input().strip()

            if command.lower() == "q":
                break

            if command.lower() == "s":
                ser.write(b"s\n")
                continue

            try:
                int(command)
                ser.write((command + "\n").encode("utf-8"))
            except ValueError:
                print("Enter an integer RPM, 's', or 'q'.")

    except KeyboardInterrupt:
        pass

    stop_flag.set()
    print("\nLogger stopped.")