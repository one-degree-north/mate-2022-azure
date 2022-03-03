#include <Servo.h>

Servo motFR;
Servo motBR;
Servo motBL;
Servo motFL;
Servo motR;
Servo motL;
Servo claw_rotate;
Servo claw_grab;  

void setup() {
  Serial.begin(9600);
  
  claw_rotate.attach(13);
  claw_grab.attach(14);
  
  motFR.attach(7, 1000, 2000);  
  motBR.attach(8, 1000, 2000);
  motBL.attach(9, 1000, 2000);
  motFL.attach(10, 1000, 2000);
  motR.attach(11, 1000, 2000);
  motL.attach(12, 1000, 2000);
  
  motFR.writeMicroseconds(1500);
  motBR.writeMicroseconds(1500);
  motBL.writeMicroseconds(1500);
  motFL.writeMicroseconds(1500);
  motR.writeMicroseconds(1500);
  motL.writeMicroseconds(1500);
  
  delayMicroseconds(5000);
  while (!Serial);
}

void loop() {
  if(Serial.available() >= 3){
    byte header = Serial.read();
    if (header == 1){
      int motor = Serial.read();
      int8_t m = Serial.read();   
      if (m == 0){
        m = 1500;
      }
      else if (m < 0){ 
        m = map(m, -127, -1, 1000, 1499);
      }
      else if (m > 0){
        m = map(m, 1, 127, 1501, 2000);
      }   
      if (motor == 2){
        motFR.writeMicroseconds(m);
      } 
      else if (motor == 3){
        motFL.writeMicroseconds(m);
      } 
      else if (motor == 4){
        motBR.writeMicroseconds(m);
      } 
      else if (motor == 5){
        motBL.writeMicroseconds(m);
      } 
      else if (motor == 6){
        motR.writeMicroseconds(m);
      } 
      else if (motor == 7){
        motL.writeMicroseconds(m);
      }
      else if (motor == 13){
        if (m == 127){
          motFR.writeMicroseconds(2000);
          motFL.writeMicroseconds(2000);
          motBR.writeMicroseconds(2000);
          motBL.writeMicroseconds(2000);
        }
        else if (m == 254){
          motFR.writeMicroseconds(1000);
          motFL.writeMicroseconds(1000);
          motBR.writeMicroseconds(1000);
          motBL.writeMicroseconds(1000);
        }
        else if (m == 0){
          motFR.writeMicroseconds(1500);
          motFL.writeMicroseconds(1500);
          motBR.writeMicroseconds(1500);
          motBL.writeMicroseconds(1500);
      }
    }
  }
   reportIMUData();
}
void reportIMUData() {
    sensors_event_t event; 
    bno.getEvent(&event);
    sensors_event_t orientation, gyro, accel;
    bno.getEvent(&orientation, Adafruit_BNO055::VECTOR_EULER);
    bno.getEvent(&gyro, Adafruit_BNO055::VECTOR_GYROSCOPE);
    bno.getEvent(&accel, Adafruit_BNO055::VECTOR_LINEARACCEL);

    Serial.write(0xA4);
  
    Serial.write(orientation.orientation.x);
    Serial.write(orientation.orientation.y);
    Serial.write(orientation.orientation.z);
    Serial.write(gyro.gyro.x);
    Serial.write(gyro.gyro.y);
    Serial.write(gyro.gyro.z);
    Serial.write(accel.acceleration.x);
    Serial.write(accel.acceleration.y);
    Serial.write(accel.acceleration.z);

    Serial.write(0x56);
}
