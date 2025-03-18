# Proyecto de Seguimiento de Postura y Control de Robot Humanoide

## Descripción
Este proyecto permite el seguimiento de la postura humana utilizando MediaPipe y OpenCV, para posteriormente enviar los ángulos de las articulaciones a un robot humanoide controlado por un ESP32. El ESP32 recibe los datos a través de una conexión serial y ajusta los servomotores en consecuencia.

## Características
- Detección de postura en tiempo real con MediaPipe y OpenCV.
- Cálculo de ángulos de articulaciones clave (hombros, codos y muñecas).
- Envío de datos de postura al ESP32 mediante una conexión serial.
- Control de servomotores en el ESP32 con la biblioteca `ESP32Servo`.
- Posibilidad de usar Bluetooth para la comunicación con el ESP32.

## Requisitos
### En la PC:
- Python 3.8+
- OpenCV
- MediaPipe
- PySerial
- PlatformIO (para la compilación del ESP32)
- Una cámara web

### En el ESP32:
- PlatformIO
- Biblioteca `ESP32Servo`
- Servomotores conectados a los pines especificados

## Instalación
### Configuración del entorno Python
```bash
pip install opencv-python mediapipe pyserial
```

### Configuración del ESP32
1. Conectar el ESP32 a la PC mediante USB.
2. Instalar PlatformIO si no está instalado:
   ```bash
   pip install platformio
   ```
3. Compilar y subir el firmware al ESP32:
   ```bash
   pio run --target upload
   ```

## Uso
1. Ejecutar el script de detección en la PC:
   ```bash
   python main.py
   ```
2. Asegurar que el ESP32 esté conectado y recibiendo datos.
3. Observar la postura detectada y el movimiento de los servomotores en el robot.
