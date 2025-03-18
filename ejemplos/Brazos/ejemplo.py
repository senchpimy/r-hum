import serial
import struct
import time

fmt = "hhhhhh"

ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)

joint_data = (120, 90, 45, 130, 85, 40)

packed_data = struct.pack(fmt, *joint_data)

try:
    while True:
        ser.write(packed_data)

        print(f"Sent: {joint_data}")

        time.sleep(1)
        while ser.in_waiting:
            try:
                line = ser.readline().decode("utf-8").strip()
                print(f"Received: {line}")
            except:
                pass

except KeyboardInterrupt:
    print("Exiting...")

finally:
    ser.close()
