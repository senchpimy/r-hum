import serial
import struct
import time


# joint_data = (120, 90, 45, 130, 85, 40)


class Sender:
    def __init__(self) -> None:
        self.fmt = "hhhhhh"
        while True:
            print("Esperando dispositivo")
            try:
                self.ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
                return
            except:
                print("Dispositivo no encontrado")
                time.sleep(2)

    def send(
        self,
        shoulder_rigth_ang,
        elbow_rigt_ang,
        wrist_rigth_ang,
        shoulder_left_ang,
        elbow_left_ang,
        wrist_left_ang,
    ):
        data = [
            shoulder_rigth_ang,
            elbow_rigt_ang,
            wrist_rigth_ang,
            shoulder_left_ang,
            elbow_left_ang,
            wrist_left_ang,
        ]
        packed_data = struct.pack(self.fmt, *data)
        try:
            self.ser.write(packed_data)

            print(f"Sent: {data}")

            while self.ser.in_waiting:
                try:
                    line = self.ser.readline().decode("utf-8").strip()
                    print(f"Received: {line}")
                except:
                    pass

        except Exception as error:
            print("An exception occurred:", error)
            print("Exiting...")

        finally:
            pass
            # self.ser.close()
