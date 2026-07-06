/*
 * Drive controller firmware for the FIRA autonomous RC car.
 *
 * Reads line-based commands over USB-serial from serial_bridge_node.py
 * (ros_ws/src/fira_car_control/fira_car_control/serial_bridge_node.py)
 * and drives the MG90s steering servo + DC-motor-280 H-bridge accordingly.
 *
 * Protocol (newline-terminated ASCII, matches serial_bridge_node.py):
 *   S<angle_deg>   e.g. "S97.50"  -> steering servo target angle
 *   T<throttle>    e.g. "T0.42"   -> motor throttle, -1.0..1.0
 *                                    (negative = reverse, 0 = stop)
 *
 * This is a fresh implementation, not a port of the referenced
 * COONEO/Arduino_Raspberry_ROS_Car code (that project drives a 4-wheel
 * differential robot with encoders/PID over rosserial, a different drive
 * architecture from this Ackermann-steering RC car) and not a port of
 * tommybee456/ESP32-Car-Project (that firmware is for a hand-held RC
 * remote over ESP-NOW, not for commands coming from an onboard computer).
 *
 * Target board: Arduino Uno/Nano + a generic 2-pin-direction H-bridge
 * (e.g. L298N/TB6612). If an ESP32 is used instead (as in the model
 * author's own board), swap analogWrite()/Servo for the ESP32 LEDC API —
 * see docs/electronics-bom.md for the ESP32 PWM parameters observed in
 * tommybee456's firmware (50 Hz / 10-bit for the servo, 1 kHz for the
 * motor) as a tuning reference.
 *
 * UNTESTED ON REAL HARDWARE: no microcontroller/H-bridge/servo was
 * available at the time this was written (see roadmap issue #5). Pin
 * numbers below are placeholders to be adjusted to the actual wiring once
 * hardware from issue #1 arrives.
 */

#include <Servo.h>

// --- Pin configuration (placeholder, confirm against real wiring) ---
const int STEERING_SERVO_PIN = 9;
const int MOTOR_IN1_PIN = 5;   // direction pin 1
const int MOTOR_IN2_PIN = 6;   // direction pin 2
const int MOTOR_PWM_PIN = 3;   // speed (PWM), only needed if H-bridge
                                // has a separate enable/PWM pin

// --- Steering limits (match steering_control_node.py defaults) ---
const float STEERING_CENTER_DEG = 90.0;
const float STEERING_MIN_DEG = 60.0;
const float STEERING_MAX_DEG = 120.0;

// --- Safety timeout: stop the motor if no command arrives for this long.
// This matters specifically because the car is meant to run autonomously —
// if the onboard Pi/Jetson crashes or the serial link drops, the car must
// not keep driving on the last throttle value it received. ---
const unsigned long COMMAND_TIMEOUT_MS = 500;

Servo steeringServo;
unsigned long lastCommandMillis = 0;

void setup() {
  Serial.begin(115200);

  steeringServo.attach(STEERING_SERVO_PIN);
  steeringServo.write(STEERING_CENTER_DEG);

  pinMode(MOTOR_IN1_PIN, OUTPUT);
  pinMode(MOTOR_IN2_PIN, OUTPUT);
  pinMode(MOTOR_PWM_PIN, OUTPUT);
  stopMotor();

  lastCommandMillis = millis();
}

void loop() {
  readSerialCommands();

  if (millis() - lastCommandMillis > COMMAND_TIMEOUT_MS) {
    stopMotor();
  }
}

void readSerialCommands() {
  static String line;

  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n') {
      handleLine(line);
      line = "";
    } else if (c != '\r') {
      line += c;
    }
  }
}

void handleLine(const String &line) {
  if (line.length() < 2) {
    return;
  }

  char command = line.charAt(0);
  float value = line.substring(1).toFloat();

  if (command == 'S') {
    setSteering(value);
    lastCommandMillis = millis();
  } else if (command == 'T') {
    setThrottle(value);
    lastCommandMillis = millis();
  }
}

void setSteering(float angleDeg) {
  angleDeg = constrain(angleDeg, STEERING_MIN_DEG, STEERING_MAX_DEG);
  steeringServo.write(angleDeg);
}

void setThrottle(float throttle) {
  throttle = constrain(throttle, -1.0, 1.0);

  if (throttle > 0.0) {
    digitalWrite(MOTOR_IN1_PIN, HIGH);
    digitalWrite(MOTOR_IN2_PIN, LOW);
  } else if (throttle < 0.0) {
    digitalWrite(MOTOR_IN1_PIN, LOW);
    digitalWrite(MOTOR_IN2_PIN, HIGH);
  } else {
    digitalWrite(MOTOR_IN1_PIN, LOW);
    digitalWrite(MOTOR_IN2_PIN, LOW);
  }

  int pwmValue = (int)(fabs(throttle) * 255.0);
  analogWrite(MOTOR_PWM_PIN, pwmValue);
}

void stopMotor() {
  digitalWrite(MOTOR_IN1_PIN, LOW);
  digitalWrite(MOTOR_IN2_PIN, LOW);
  analogWrite(MOTOR_PWM_PIN, 0);
}
