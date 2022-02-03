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
      else if (motor == 11){
        motFR.writeMicroseconds(m);
        motFL.writeMicroseconds(m);
        motBR.writeMicroseconds(m);
        motBL.writeMicroseconds(m);
        motR.writeMicroseconds(m);
        motL.writeMicroseconds(m);
      }
      else if (motor == 13){
        motFR.writeMicroseconds(m);
        motFL.writeMicroseconds(m);
        motBR.writeMicroseconds(m);
        motBL.writeMicroseconds(m);
      }
      else if (motor == 14){
        motFR.writeMicroseconds(m);
        motFL.writeMicroseconds(m);
        motBR.writeMicroseconds(m);
        motBL.writeMicroseconds(m);
      }
    }
  }
}
