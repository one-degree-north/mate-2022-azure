


#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <Servo.h>
char header = 1
char footer = 10
  
Servo mythruster_VL;
Servo mythruster_VR;
Servo mythruster_R;
Servo mythruster_L;
Servo myservo_rotate;
Servo myservo_grab;  


void setup() {
  myservo_rotate.attach(13);
  myservo_grab.attach(14);
  
  mythruster_VL.attach(9,1000,2000);
  mythruster_VL.writeMicroseconds(1500);
  
  mythruster_VR.attach(10,1000,2000);
  mythruster_VR.writeMicroseconds(1500);
  
  mythruster_R.attach(11,1000,2000);
  mythruster_R.writeMicroseconds(1500);
  
  mythruster_L.attach(12,1000,2000);
  mythruster_L.writeMicroseconds(1500);
  
  delay(200);
  Serial.begin(9600);
}

void loop() {
  /*sensors_event_t orientationData , angVelocityData , linearAccelData, magnetometerData, accelerometerData, gravityData;
  bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
  bno.getEvent(&angVelocityData, Adafruit_BNO055::VECTOR_GYROSCOPE);
  bno.getEvent(&linearAccelData, Adafruit_BNO055::VECTOR_LINEARACCEL);

  printEvent(&orientationData);
  printEvent(&angVelocityData);
  printEvent(&linearAccelData);

  int8_t boardTemp = bno.getTemp();
  Serial.println();
  Serial.print(F("temperature: "));
  Serial.println(boardTemp);

  uint8_t system, gyro, accel, mag = 0;
  bno.getCalibration(&system, &gyro, &accel, &mag);
  Serial.println();
  Serial.print("Calibration: Sys=");
  Serial.print(system);
  Serial.print(" Gyro=");
  Serial.print(gyro);
  Serial.print(" Accel=");
  Serial.print(accel);
  Serial.print(" Mag=");
  Serial.println(mag);

  Serial.println("--");
  delay(BNO055_SAMPLERATE_DELAY_MS);*/

    if (Serial.available()>=4){
      byte packetheader = Serial.read();
      byte motor = Serial.read();
      byte speed = Serial.read();
      byte packetfooter = Serial.read();
      
      if (packetheader == 1 and packetfooter == 10){
        int motor_speed = 10 * speed;
        if (motor == 2){
          mythruster_VR.writeMicroseconds(motor_speed);
        } else if (motor == 3){
          mythruster_VL.writeMicroseconds(motor_speed);
        } else if (motor == 5){
          mythruster_R.writeMicroseconds(motor_speed);
        } else if (motor == 6){
          mythruster_L.writeMicroseconds(motor_speed);
        } else if (motor == 7){
          motor_speed = map(motor_speed, 100, 200, 0, 180);
          myservo_rotate.write(motor_speed);
        } else if (motor == 8){
          motor_speed = map(motor_speed, 100, 200, 0, 180);
          myservo_grab.write(motor_speed);
        } else if (motor == 14){
          motor_speed = 150
          mythruster_VR.writeMicroseconds(motor_speed);
          mythruster_VL.writeMicroseconds(motor_speed);
          mythruster_R.writeMicroseconds(motor_speed);
          mythruster_L.writeMicroseconds(motor_speed);
          
          servo_setting = 90;
          myservo_grab.write(servo_setting);
          myservo_rotate.write(servo_setting);
        }
      }
    }
}

void printEvent(sensors_event_t* event) {
  double x = -1000000, y = -1000000 , z = -1000000; //dumb values, easy to spot problem
  else if (event->type == SENSOR_TYPE_ORIENTATION) {
    Serial.print("Orient:");
    x = event->orientation.x;
    y = event->orientation.y;
    z = event->orientation.z;
  }
  else if (event->type == SENSOR_TYPE_GYROSCOPE) {
    Serial.print("Gyro:");
    x = event->gyro.x;
    y = event->gyro.y;
    z = event->gyro.z;
  }
  else if (event->type == SENSOR_TYPE_ROTATION_VECTOR) {
    Serial.print("Rot:");
    x = event->gyro.x;
    y = event->gyro.y;
    z = event->gyro.z;
  }
  else if (event->type == SENSOR_TYPE_LINEAR_ACCELERATION) {
    Serial.print("Linear:");
    x = event->acceleration.x;
    y = event->acceleration.y;
    z = event->acceleration.z;
  }
  else {
    Serial.print("Unk:");
  }

  Serial.print("\tx= ");
  Serial.print(x);
  Serial.print(" |\ty= ");
  Serial.print(y);
  Serial.print(" |\tz= ");
  Serial.println(z);
}


               
/*void mythruster_setup() {
  mythruster_BL.writeMicroseconds((int (incomingByte[2])/255)*500+1500));
}*/
  
  
