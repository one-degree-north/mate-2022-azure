#include <Servo.h>
Servo myservo;

int thruster_Speed = 1500;
Servo mythruster;
int pos = 0;
void setup() {
  mythruster.attach(7);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  mythruster.writeMicroseconds(1500);
  delay(200);
  Serial.begin(9600);

 
}

void loop() {
  myservo.write(0);              // tell servo to go to position in variable 'pos'


  Serial.print("Enter thruster speed: ");
  int temp = Serial.parseInt();
  if (temp != 0) thruster_Speed = temp;
  //changing the fan speed
  Serial.print("thruster_speed = ");
  Serial.println(thruster_Speed);
  mythruster.writeMicroseconds(thruster_Speed);
  Serial.write(9600);
  Serial.available();
  myservo.write(45);              // tell servo to go to position in variable 'pos'
  delay(300);

}
