#include <Arduino.h>
#include <ESP32Servo.h>
#include <cstdint>

struct Robot {
  int16_t right_shoulder;
  int16_t right_elbow;
  int16_t right_wrist;
  int16_t left_shoulder;
  int16_t left_elbow;
  int16_t left_wrist;
};

struct RobotServo {
  Servo right_shoulder_s;
  Servo right_elbow_s;
  Servo right_wrist_s;
  Servo left_shoulder_s;
  Servo left_elbow_s;
  Servo left_wrist_s;
  int init(int right_shoulder, int right_elbow, int right_wrist,
           int left_shoulder, int left_elbow, int left_wrist) {
    right_shoulder_s.attach(right_shoulder);
    right_elbow_s.attach(right_elbow);
    right_wrist_s.attach(right_wrist);
    left_shoulder_s.attach(left_shoulder);
    left_elbow_s.attach(left_elbow);
    left_wrist_s.attach(left_wrist);
    return 0;
  }
  int write(Robot *r) {
    right_shoulder_s.write(r->right_shoulder);
    right_elbow_s.write(r->right_elbow);
    right_wrist_s.write(r->right_wrist);
    left_shoulder_s.write(r->left_shoulder);
    left_elbow_s.write(r->left_elbow);
    left_wrist_s.write(r->left_wrist);
    return 0;
  }
};

Robot robot;
RobotServo robot_servo;

#define RIGHT_SHOULDER_PIN 13
#define RIGHT_ELBOW_PIN 12
#define RIGHT_WRIST_PIN 2
#define LEFT_SHOULDER_PIN 14
#define LEFT_ELBOW_PIN 27
#define LEFT_WRIST_PIN 2
void setup() {
  Serial.begin(115200);

  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  robot_servo.init(RIGHT_SHOULDER_PIN, RIGHT_ELBOW_PIN, RIGHT_WRIST_PIN,
                   LEFT_SHOULDER_PIN, LEFT_ELBOW_PIN, LEFT_WRIST_PIN);
}
void loop() {
  if (Serial.available() >= sizeof(Robot)) {
    Serial.readBytes((char *)&robot, sizeof(Robot));
    robot_servo.write(&robot);
    Serial.println("Robot joint positions:");
    Serial.print("Right Shoulder: ");
    Serial.println(robot.right_shoulder);
    Serial.print("Right Elbow: ");
    Serial.println(robot.right_elbow);
    Serial.print("Right Wrist: ");
    Serial.println(robot.right_wrist);
    Serial.print("Left Shoulder: ");
    Serial.println(robot.left_shoulder);
    Serial.print("Left Elbow: ");
    Serial.println(robot.left_elbow);
    Serial.print("Left Wrist: ");
    Serial.println(robot.left_wrist);
  }
}
