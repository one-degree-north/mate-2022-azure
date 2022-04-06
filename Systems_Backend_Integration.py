from threading import Thread
import serial
#import struct

class Comms:
    def __init__(self, port: str, baud_rate: int):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = serial.Serial(self.port, self.baud_rate)
        self.ser.close()
        self.ser.open()

    def run(self):
        self.command = input("Enter Command: ")
        if (self.command == "LeftJoyForward"):
            #tell both thrusters to move forward
            print("GOT COMMAND")
            packet_rightThruster = chr(1) + chr(6) + chr(200) + chr(255)
            self.ser.write(packet_rightThruster.encode("latin"))
            packet_leftThruster = chr(1) + chr(7) + chr(200) + chr(255)
            self.ser.write(packet_leftThruster.encode("latin"))

        if (self.command == "LeftJoyBackwards"):
            #tell thrusters to move backwards
            packet_rightThrus = chr(1) + chr(6) + chr(120) + chr(255) 
            self.ser.write(packet_rightThrus.encode("latin"))
            packet_leftThurs = chr(1) + chr(7) + chr(120) + chr(255) 
            self.ser.write(packet_leftThurs.encode("latin"))

        #coding left and right movement
        if (self.command == "RightJoyRight"):
            #joystick has been moved to the right - code left thruster to move
            packet_leftThruster = chr(1) + chr(6) + chr(150) + chr(255)
            self.ser.write(packet_leftThruster.encode("latin"))
            #right thruster going the other way
            packet_rightThruster = chr(1) + chr(7) + chr(104) + chr(255)
            self.ser.write(packet_rightThruster.encode("latin"))

        if (self.command == "RightJoyLeft"):  
            #joystick has been moved to the left - code right thruster to move
            packet_rightThruster = chr(1) + chr(6) + chr(150) + chr(255)
            self.ser.write(packet_rightThruster.encode("latin"))
            #left thruster goes the other way
            packet_leftThruster = chr(1) + chr(7) + chr(104) + chr(255)
            self.ser.write(packet_leftThruster.encode("latin"))

        #servo claw code
        #chr(11) tells systems to switch off the servo and chr(12) tells to switch on
        if (self.command == "APressed"):
            packet_servoRotate = chr(1) + chr(8) + chr(11) + chr(255)
            self.ser.write(packet_servoRotate.encode("latin"))
        else:
            packet_servoRotate_off = chr(1) + chr(8) + chr(11) + chr(255)
            self.ser.write(packet_servoRotate_off.encode("latin"))

        '''
        #not working for now so just ignore
        if (self.command == True):
            packet_servoGrab = chr(1) + chr(9) + chr(12) + chr(255)
            self.ser.write(packet_servoGrab.encode("latin"))
        else:
            packet_servoGrab_off = chr(1) + chr(9) + chr(11) + chr(255)
            self.ser.write(packet_servoGrab_off.encode("latin"))
        '''

        #4 up and down 
        if (self.command == "RightTrigger"):
            #4 motors go up
            packet_RB_up = chr(1) + chr(13) + chr(127) + chr(255)
            self.ser.write(packet_RB_up.encode("latin"))
        if (self.command == "LeftTrigger"):
            #4 motors go down
            packet_LB_up = chr(1) + chr(13) + chr(254) + chr(255)
            self.ser.write(packet_LB_up.encode("latin"))

        if (self.command == "Kill"):
            packet_killSwitch = chr(1) + chr(14) + chr(100) + chr(255)
            self.ser.write(packet_killSwitch.encode("latin"))

        if (self.command == "Flush"):
            self.ser.write("88888".encode("latin"))
        #second byte chr(14) means kill all operations, while chr(100) is just an empty byte
        
        '''
        #to recieve the gyroscope information from systems
        packet_IMUdata = self.Serial.read(size=4)
        #orien = []
        #if defined earlier, orien.x and etc for object orien will work; self just defines/declares the unpacked variable
        header, self.orien.x, self.orien.y, self.orien.z, self.gyro.x, self.gyro.y, self.gyro.z, self.accel.x, self.accel.y, self.accel.z = struct.unpack('ccfffffffff')  
        '''

test = Comms("/dev/tty.usbserial-1110", 9600)
while True:
    test.run()
