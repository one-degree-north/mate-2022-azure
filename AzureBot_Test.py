from threading import Thread
import serial
import controls
import gui
import struct

class Comms:
    def __init__(self, port: str, baud_rate: int):
        self.port = port
        self.baud_rate = baud_rate
        ser = serial.Serial(self.port, self,baud_rate)
        self.ser.close()
        self.ser.open()

    def send_value(self,value):
        #preq: -100<=value<=100
        value = round(value*1.27)
        if value<0:
            value = 255+value
        return value 

    def run(self):
        while True: 
            packetControls = controls.Controls() #change later
            #leftJoy_LR = packetControls.packet[0] #and repeat... will finalize once I know what values will come
            leftJoy_UD = packetControl.packet[1]
            rightJoy_LR = packetControls.packet[2]
            #rightJoy_UD = packetControls.packet[3]
            servoRotate = packetControls.packet[4]
            servoGrab = packetControls.packet[5]
            LB_up = packetControls.packets[6]
            RB_down = packetControls.packet[7]

        while True:
            #coordinate => [x,y]
            if leftJoy_UD[1] > 0 
                #joystick has been moved up; tell both thrusters to move forward 
                value = self.send_value(leftJoy_UD)
                packet_rightThruster = chr(1) + chr(6) + chr((self.value).encode("latin")) + chr(255)
                self.ser.write(packet_rightThruster)
                packet_leftThruster = chr(1) + chr(7) + chr((self.value).encode("latin")) + chr(255)
                self.ser.write(packet_leftThruster)
            else:
                if leftJoy_UD[1] < 0
                    packet_rightThrus = chr(1) + chr(6) + chr((self.value).encode("latin")) + chr(255) 
                    self.ser.write(packet_rightThrus)
                    packet_leftThurs = chr(1) + chr(7) + chr((self.value).encode("latin")) + chr(255) 
                    self.ser.write(packet_leftThurs)
            #have to specify to elimate packets being sent when joystick is at (0,0)
            

            #coding left and right movement
            if rightJoy_LR[0] > 0
                #joystick has been moved to the right
                value = self.send_value(leftJoy_UD)
                packet_rightThruster = chr(1) + chr(6) + chr((self.value).encode("latin")) + chr(255)
                self.ser.write(packet_rightThruster)
                packet_leftThruster = chr(1) + chr(7) + chr((self.value).encode("latin")) + chr(255)
                self.ser.write(packet_leftThruster)
            else: 
                if rightJoy_LR[0] < 0
                #joystick has been moved to the left
                value = self.send_value(leftJoy_UD)
                packet_rightThruster = chr(1) + chr(6) + chr((self.value).encode("latin")) + chr(255)
                self.ser.write(packet_rightThruster)
                packet_leftThruster = chr(1) + chr(7) + chr((self.value).encode("latin")) + chr(255)
                self.ser.write(packet_leftThruster)


            #previous code (reviewed and accepted - IGNORE)
            '''
            while True:
                #coding the thrusters forward and back (sendSystemsLes)
                if leftJoy_UD < [43,43]:
                    value = self.send_value(leftJoy_UD)
                    packet_leftJoy_stopped = chr(1) + chr(7) + chr((self.value).encode("latin")) + chr(255)
                    self.ser.write(packet_leftJoy_stopped)
                else:
                    value = self.send_value(leftJoy_LR)
                    packet_leftJoy = chr(1) + chr(7) + chr((self.value).encode("latin")) + chr(255) 
                    self.ser.write(packet_leftJoy)

                #coding the Right thruster
                if rightJoy_LR < [43,43]:
                    value = self.send_value(rightJoy_LR)
                    packet_rightJoy_stopped = chr(1) + chr(6) + chr((self.value).encode("latin")) + chr(255)
                    self.ser.write(packet_rightJoy_stopped)
                else:
                    packet_rightJoy = chr(1) + chr(6) + chr((self.value).encode("latin")) + chr(255) 
                    self.ser.write(packet_rightJoy)
                '''

                #servo claw code - finalized with packet value. chr(11) tells systems to switch off the servo and chr(12) is an empty byte
                if servoRotate == True:
                    value = self.send_value(servoRotate)
                    packet_servoRotate = chr(1) + chr(8) + chr(12) + chr(255)
                    self.ser.write(packet_servoRotate)
                else:
                    packet_servoRotate_off = chr(1) + chr(8) + chr(11) + chr(255)

                if servoGrab == True:
                    value = self.send_value(servoGrab)
                    packet_servoGrab = chr(1) + chr(9) + chr(12) + chr(255)
                    self.ser.write(packet_servoGrab)
                else:
                    packet_servoGrab_off = chr(1) + chr(9) + chr(11) + chr(255)

                
                #take data, convert it, and send to systems
                #[-127,127]
                

                #4 up and down motors 
                if LB_up == True:
                    packet_LB_up = chr(1) + chr(13) + chr(12) + chr(255)
                else:
                    if RB_up == True:
                        packet_RB_up = chr(1) + chr(14) + chr(12) + chr(255)
                #systems will read chr(13) and turn all 4 up-down motors up, and the chr(14) will turn them all down.

                

                #to recieve information from systems
                packet_IMUdata = self.Serial.read(size=4)
                header, orien_x, orien_y, orien_x, gyro.x, gyro.y, gyro.z, accel.x, accel.y, accel.z = struct.unpack('ccfffffffff')
                

    def start_thread(self):
        start_thread = Thread(target = self.run)  
        start_thread.start()
    
    #display_GUI = gui.GUI()

