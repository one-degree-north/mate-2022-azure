#define Serial Serial1
#include <Servo.h>
#include "Adafruit_BNO055.h"

Servo motFR;
Servo motBR;
Servo motBL;
Servo motFL;
Servo motR;
Servo motL;
Servo claw_servo;

void setup() {
  Serial.begin(9600);
  
  claw_servo.attach(12);
  
  motFR.attach(A5, 1000, 2000);  
  motBR.attach(A2, 1000, 2000);
  motBL.attach(A4, 1000, 2000);
  motFL.attach(A3, 1000, 2000);
  motR.attach(10, 1000, 2000);
  motL.attach(5, 1000, 2000);
  
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
  if(Serial.available() >= 4){
    byte header = Serial.read();
    if (header == 1){
      uint8_t motor = Serial.read();
      uint8_t m = Serial.read();   
      byte footer = Serial.read();

      if (footer != 255) return;
      
      if (m == 0){
        m = 1500;
      }
      /*else if (m < 0){ 
        m = map(m, -127, -1, 1000, 1499);
      }
      else if (m > 0){
        m = map(m, 1, 127, 1501, 2000);
      }
      
      if (m == 0){
        m = 1500;
      }
      else if (m < 0){ 
        m = map(m, -127, -1, 1000, 1499);
      }
      else if (m > 0){
        m = map(m, 1, 127, 1501, 2000);
      }   */
      if (motor == 2){
        motFR.writeMicroseconds(m * 10);
        motFL.writeMicroseconds(m * 10);
        Serial.print("Motor FR+FL");
      } 
      else if (motor == 3){
        motBR.writeMicroseconds(m * 10);
        motBL.writeMicroseconds(m * 10);
        Serial.print("Motor BR+BL");
      } 
      /*else if (motor == 4){
        motBR.writeMicroseconds(m * 10);
        Serial.print("Motor BR");
      } 
      else if (motor == 5){
        motBL.writeMicroseconds(m * 10);
        Serial.print("Motor BL");
      } */
      else if (motor == 6){
        motR.writeMicroseconds(m * 10);
        Serial.print("Motor R");
      } 
      else if (motor == 7){
        motL.writeMicroseconds(m * 10);
        Serial.print("Motor L");
      }
      else if (motor == 13){
        if (m == 127){
          motFR.writeMicroseconds(1700);
          motFL.writeMicroseconds(1700);
          motBR.writeMicroseconds(1700);
          motBL.writeMicroseconds(1700);
          Serial.print("Top Motors Up");
        }
        else if (m == 254){
          motFR.writeMicroseconds(1300);
          motFL.writeMicroseconds(1300);
          motBR.writeMicroseconds(1300);
          motBL.writeMicroseconds(1300);
          Serial.print("Top Motors Down");
        }
        else if (m == 0){
          motFR.writeMicroseconds(1500);
          motFL.writeMicroseconds(1500);
          motBR.writeMicroseconds(1500);
          motBL.writeMicroseconds(1500);
          Serial.print("Top Motors Off");
        }
      }
      else if (motor == 14){
          motFR.writeMicroseconds(1500);
          motFL.writeMicroseconds(1500);
          motBR.writeMicroseconds(1500);
          motBL.writeMicroseconds(1500);
          motR.writeMicroseconds(1500);
          motL.writeMicroseconds(1500);
          Serial.print("Motors Kill");
      }
      else if (motor == 9){
        if (m == 11){
          claw_servo.write(0);
          Serial.print("Claw Close");
        }
          if (m == 12){
          claw_servo.write(120);
          Serial.print("Claw Open");
        }
      }
    }
  }
}
