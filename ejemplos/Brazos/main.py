import os
import math
import coneccion

from collections import deque


class Promedio:
    def __init__(self):
        # Inicializa una cola de longitud máxima 5
        self.valores = deque(maxlen=5)

    def promedio(self, valor: int) -> float:
        """
        Agrega un valor y retorna el promedio de los últimos 5 valores.
        """
        self.valores.append(valor)
        return sum(self.valores) / len(self.valores)


os.environ["QT_QPA_PLATFORM"] = "xcb"
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

sender = coneccion.Sender()


class Coord:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


def calcular_angulo(a: Coord, b: Coord, c: Coord) -> int:
    vecotr_ab = (b.x - a.x, b.y - a.y)
    vecotr_bc = (c.x - b.x, c.y - b.y)
    mul_ab_bc = (vecotr_ab[0] * vecotr_bc[0]) + (vecotr_ab[1] * vecotr_bc[1])
    mag_ab = math.sqrt((vecotr_ab[0] ** 2) + (vecotr_ab[1] ** 2))
    mag_bc = math.sqrt((vecotr_bc[0] ** 2) + (vecotr_bc[1] ** 2))
    try:
        cos_ang = mul_ab_bc / (mag_ab * mag_bc)  # Might error
    except:
        cos_ang = 0
    angulo = math.acos(cos_ang)
    angulo_grados = math.degrees(angulo)

    if angulo_grados > 180:
        angulo_grados = 360 - angulo_grados

    res = int(180 - angulo_grados)
    return res if res > 10 else 10


class Body:
    def __init__(self, results, img_height: int, img_width: int):
        puntos = [
            mp_pose.PoseLandmark.RIGHT_HIP,
            mp_pose.PoseLandmark.RIGHT_SHOULDER,
            mp_pose.PoseLandmark.RIGHT_ELBOW,
            mp_pose.PoseLandmark.RIGHT_WRIST,
            mp_pose.PoseLandmark.LEFT_HIP,
            mp_pose.PoseLandmark.LEFT_SHOULDER,
            mp_pose.PoseLandmark.LEFT_ELBOW,
            mp_pose.PoseLandmark.LEFT_WRIST,
        ]

        nombres_puntos = [
            "RIGHT_HIP",
            "RIGHT_SHOULDER",
            "RIGHT_ELBOW",
            "RIGHT_WRIST",
            "LEFT_HIP",
            "LEFT_SHOULDER",
            "LEFT_ELBOW",
            "LEFT_WRIST",
        ]

        self.elementos = []
        for i, nombre in zip(puntos, nombres_puntos):
            try:
                x = int(results.pose_landmarks.landmark[i].x * img_width)
                y = int(results.pose_landmarks.landmark[i].y * img_height)
                p = (x, y) if 0 <= x < img_width and 0 <= y < img_height else None
                if p is not None:
                    p = Coord(p[0], p[1])
            except AttributeError:
                p = None
            setattr(self, nombre, p)
            self.elementos.append(p)
        if self.angulo():
            sender.send(
                self.shoulder_rigth_ang,
                self.elbow_rigth_ang,
                0,
                self.shoulder_left_ang,
                self.elbow_left_ang,
                0,
            )

    def angulo(self):
        a = self.RIGHT_SHOULDER
        b = self.RIGHT_ELBOW
        c = self.RIGHT_WRIST

        d = self.LEFT_SHOULDER
        e = self.LEFT_ELBOW
        f = self.LEFT_WRIST
        if None in [a, b, c, d, e, f]:
            return
        self.elbow_rigth_ang = calcular_angulo(a, b, c)
        self.elbow_left_ang = calcular_angulo(d, e, f)

        a = self.RIGHT_HIP
        b = self.RIGHT_SHOULDER
        c = self.RIGHT_ELBOW

        d = self.LEFT_HIP
        e = self.LEFT_SHOULDER
        f = self.LEFT_ELBOW
        if None in [a, b, c, d, e, f]:
            return
        self.shoulder_rigth_ang = calcular_angulo(a, b, c)
        self.shoulder_left_ang = calcular_angulo(d, e, f)
        print(self.shoulder_left_ang)
        print(self.shoulder_rigth_ang)
        return 1

    def send(self):
        pass


def crear_cuerpo(results, img_height: int, img_width: int):
    b = Body(results, img_height, img_width)
    result = False
    if None in b.elementos:
        result = True
    return b, result


# For webcam input:
def main():
    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(
        model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as pose:
        while cap.isOpened():
            success, image = cap.read()
            img_width = int(image.shape[1] * 1.4)
            img_height = int(image.shape[0] * 1.4)
            image = cv2.resize(image, (img_width, img_height))
            if not success:
                print("Ignoring empty camera frame.")
                continue

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
            )

            b, r = crear_cuerpo(results, img_height, img_width)
            image = cv2.flip(image, 1)
            if r:
                font = cv2.FONT_HERSHEY_SIMPLEX
                org = (50, 50)
                fontScale = 1
                color = (0, 0, 255)
                thickness = 2
                image = cv2.putText(
                    image,
                    "No se ve el cuerpo completo",
                    org,
                    font,
                    fontScale,
                    color,
                    thickness,
                    cv2.LINE_AA,
                )
            cv2.imshow("MediaPipe Pose", image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()


main()
