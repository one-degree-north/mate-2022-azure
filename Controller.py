from XInput import *

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

set_deadzone(DEADZONE_TRIGGER,10)

class Controller:
    def __init__(self, center, comms, port:str, baud_rate: int):
        self.center = center
        self.comms = comms
        self.port = port
        self.baud_rate = baud_rate
        self.ser = serial.Serial(self.port, self,baud_rate)
        self.ser.close()
        self.ser.open()
        self.on_indicator_pos = (self.center[0], self.center[1] - 50)       
        self.r_thumb_pos = (self.center[0] + 50, self.center[1] + 20)
        self.l_thumb_pos = (self.center[0] - 100, self.center[1] - 20)        
        self.l_trigger_pos = (self.center[0] - 120, self.center[1] - 70)           
        self.r_trigger_pos = (self.center[0] + 120, self.center[1] - 70)             
        self.buttons_pos = (self.center[0] + 100, self.center[1] - 20)
        self.A_button_pos = (buttons_pos[0], buttons_pos[1] + 20)
        self.B_button_pos = (buttons_pos[0] + 20, buttons_pos[1])
        self.Y_button_pos = (buttons_pos[0], buttons_pos[1] - 20)
        self.X_button_pos = (buttons_pos[0] - 20, buttons_pos[1])        
        self.dpad_pos = (self.center[0] - 50, self.center[1] + 20)
        self.back_button_pos = (self.center[0] - 20, self.center[1] - 20)
        self.start_button_pos = (self.center[0] + 20, self.center[1] - 20)
        self.l_shoulder_pos = (self.center[0] - 90, self.center[1] - 70)
        self.r_shoulder_pos = (self.center[0] + 90, self.center[1] - 70)

controllers = (Controller((150., 100.), None),
               Controller((450., 100.), None),
               Controller((150., 300.), None),
               Controller((450., 300.), None))

def send_value(self,value):
        #preq: -100<=value<=100
        self.value = round(value*1.27)
        if self.value<0:
            self.value = 255+self.value
        return self.value
     
def run(self):
    while True:
        events = get_events()
        for event in events:
            controller = controllers[event.user_index]
        
            if event.type == EVENT_STICK_MOVED:
                if event.stick == LEFT:
                    self.l_thumb_stick_pos = (int(round(controller.l_thumb_pos[0] + 25 * event.x,0)), int(round(controller.l_thumb_pos[1] - 25 * event.y,0)))
                    if self.l_thumb_stick_pos[1] > 80:
                        self.percentage_x = int(((self.l_thumb_stick_pos[1] - 80)/25)*100)
                        self.comms.packetControls.packet[1] = self.percentage_x
                        print("Robot goes backward")
                        self.value = self.send_self.value(self.percentage_x)
                        self.packet_rightThruster = chr(1) + chr(6) + chr(self.value) + chr(255)
                        self.ser.write(self.packet_rightThruster.encode("latin"))
                        self.packet_leftThruster = chr(1) + chr(7) + chr(self.value) + chr(255)
                        self.ser.write(self.packet_leftThruster.encode("latin"))
                        
                    elif self.l_thumb_stick_pos[1] < 80:
                        self.percentage_x = int(((80 - self.l_thumb_stick_pos[1])/25)*100)
                        self.comms.packetControls.packet[1] = self.percentage_x
                        print("Robot goes forward")
                        self.value = self.send_self.value(self.percentage_x)
                        self.packet_rightThruster = chr(1) + chr(6) + chr(self.value) + chr(255)
                        self.ser.write(self.packet_rightThruster.encode("latin"))
                        self.packet_leftThruster = chr(1) + chr(7) + chr(self.value) + chr(255)
                        self.ser.write(self.packet_leftThruster.encode("latin"))
                
                elif event.stick == RIGHT:
                    self.r_thumb_stick_pos = (int(round(controller.self.r_thumb_pos[0] + 25 * event.x,0)), int(round(controller.self.r_thumb_pos[1] - 25 * event.y,0)))
                    if self.r_thumb_stick_pos[0] > 200:
                        self.percentage_y = int(((self.r_thumb_stick_pos[0] - 200)/25)*100)
                        self.comms.packetControls.packet[2] = self.percentage_y
                        print("Robot goes right")
                        #joystick has been moved to the right - code left thruster to move
                        self.value_leftMot = self.send_value(self.rightJoy_LR)
                        self.packet_leftThruster = chr(1) + chr(6) + chr(self.value_leftMot) + chr(255)
                        self.ser.write(self.packet_leftThruster.encode("latin"))
                        #right thruster going the other way
                        self.value_rightMot = self.send_value(-self.rightJoy_LR)
                        self.convert_value_rightMot = (self.value_rightMot).encode("latin")
                        self.packet_rightThruster = chr(1) + chr(7) + chr(self.value_rightMot) + chr(255)
                        self.ser.write(self.packet_rightThruster.encode("latin"))
                        
                    elif self.r_thumb_stick_pos[0] < 200:
                        self.percentage_y = int(((200 - self.r_thumb_stick_pos[0])/25)*100)
                        self.comms.packetControls.packet[2] = self.percentage_y
                        print("Robot goes left")
                        #joystick has been moved to the left - code right thruster to move
                        self.value_rightMot = self.send_value(self.rightJoy_LR)
                        self.packet_rightThruster = chr(1) + chr(6) + chr(self.value_rightMot) + chr(255)
                        self.ser.write(self.packet_rightThruster.encode("latin"))
                        #left thruster goes the other way
                        self.value_leftMot = self.send_value(-self.rightJoy_LR)
                        self.packet_leftThruster = chr(1) + chr(7) + chr(self.value_leftMot) + chr(255)
                        self.ser.write(self.packet_leftThruster.encode("latin"))
                
            elif event.type == EVENT_TRIGGER_MOVED:
                if event.trigger == LEFT:
                    self.l_trigger_index_pos = (controller.l_trigger_pos[0], controller.l_trigger_pos[1] - 20 + int(round(40 * event.value, 0)))
                    print(self.l_trigger_index_pos)
                    if self.l_trigger_index_pos[1] > 30:
                        self.comms.packetControls.packet[7] = true
                        print("Robot goes down")
                        self.packet_LB_up = chr(1) + chr(13) + chr(254) + chr(255)
                        self.ser.write(self.packet_LB_up.encode("latin"))
                        
                elif event.trigger == RIGHT:
                    self.r_trigger_index_pos = (controller.r_trigger_pos[0], controller.r_trigger_pos[1] - 20 + int(round(40 * event.value, 0)))
                    print(self.r_trigger_index_pos)
                    if self.r_trigger_index_pos[1] > 30:
                        self.comms.packetControls.packet[6] = true
                        print("Robot goes up")
                        self.packet_RB_up = chr(1) + chr(13) + chr(127) + chr(255)
                        self.ser.write(self.packet_RB_up.encode("latin"))
                        
            elif event.type == EVENT_BUTTON_PRESSED:                

                if event.button == "DPAD_LEFT":
                    print("Switch to Camera 2")
                elif event.button == "DPAD_RIGHT":
                    print("Switch to Camera 3")
                elif event.button == "DPAD_UP":
                    print("Switch to Camera 1")
                elif event.button == "DPAD_DOWN":
                    print("Switch to Camera 4")

                elif event.button == "A":
                    self.comms.packetControls.packet[5] = True
                    print("Claw grabs")
                    self.packet_servoGrab = chr(1) + chr(9) + chr(12) + chr(255)
                    self.ser.write(self.packet_servoGrab.encode("latin"))
                
                '''
                elif event.button == "B":
                    self.comms.packetControls.packet[5] = False
                    print("Claw releases")
                #don't need another button since claw_rotate will currently not be used
                '''

                elif event.button == "X":
                    print("Take picture")
                
                elif event.button == "Y":
                    self.comms.packetControls.packet[7] = True
                    print("Robot is killed")
                    self.packet_killSwitch = chr(1) + chr(14) + chr(100) + chr(255)
                    self.ser.write(self.packet_killSwitch.encode("latin"))
              
            elif event.type == EVENT_BUTTON_RELEASED:                
                if event.button == "DPAD_LEFT":
                    print("Remain on Camera 2")
                elif event.button == "DPAD_RIGHT":
                    print("Remain on Camera 3")
                elif event.button == "DPAD_UP":
                    print("Remain on Camera 1")
                elif event.button == "DPAD_DOWN":
                    print("Remain on Camera 4")
                
                elif event.button == "A":
                    self.comms.packetControls.packet[5] = True
                    print("Claw stops grabbing")
                    self.packet_servoGrab_off = chr(1) + chr(9) + chr(11) + chr(255)
                    self.ser.write(self.packet_servoGrab_off.encode("latin"))
                
                '''
                elif event.button == "B":
                    self.comms.packetControl.packet[5] = False
                    print("Claw has been released")
                #don't need another button since claw_rotate will currently not be used
                '''
                
                elif event.button == "X":
                    print("Stop taking pictures")
                
                '''
                elif event.button == "Y":
                    self.comms.packetControls.packet[7] = True
                    print("Robot is killed")
                #don't need; when Y is pressed a kill packet will be sent
                '''

