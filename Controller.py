from XInput import *

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

set_deadzone(DEADZONE_TRIGGER,10)

class Controller:
    def __init__(self, center, comms):
        self.center = center
        self.comms = comms
        self.on_indicator_pos = (self.center[0], self.center[1] - 50)       
        self.r_thumb_pos = (self.center[0] + 50, self.center[1] + 20)
        self.l_thumb_pos = (self.center[0] - 100, self.center[1] - 20)        
        self.l_trigger_pos = (self.center[0] - 120, self.center[1] - 70)           
        self.r_trigger_pos = (self.center[0] + 120, self.center[1] - 70)             
        buttons_pos = (self.center[0] + 100, self.center[1] - 20)
        A_button_pos = (buttons_pos[0], buttons_pos[1] + 20)
        B_button_pos = (buttons_pos[0] + 20, buttons_pos[1])
        Y_button_pos = (buttons_pos[0], buttons_pos[1] - 20)
        X_button_pos = (buttons_pos[0] - 20, buttons_pos[1])        
        dpad_pos = (self.center[0] - 50, self.center[1] + 20)
        back_button_pos = (self.center[0] - 20, self.center[1] - 20)
        start_button_pos = (self.center[0] + 20, self.center[1] - 20)
        l_shoulder_pos = (self.center[0] - 90, self.center[1] - 70)
        r_shoulder_pos = (self.center[0] + 90, self.center[1] - 70)

controllers = (Controller((150., 100.), None),
               Controller((450., 100.), None),
               Controller((150., 300.), None),
               Controller((450., 300.), None))

while 1:
    events = get_events()
    for event in events:
        controller = controllers[event.user_index]
        
        if event.type == EVENT_STICK_MOVED:
            if event.stick == LEFT:
                l_thumb_stick_pos = (int(round(controller.l_thumb_pos[0] + 25 * event.x,0)), int(round(controller.l_thumb_pos[1] - 25 * event.y,0)))
                if l_thumb_stick_pos[1] > 80:
                    percentage_x = int(((l_thumb_stick_pos[1] - 80)/25)*100)
                    controller.comms.packetControls.packet[1] = percentage_x
                    print("Robot goes backward")
                elif l_thumb_stick_pos[1] < 80:
                    percentage_x = int(((80 - l_thumb_stick_pos[1])/25)*100)
                    controller.comms.packetControls.packet[1] = percentage_x
                    print("Robot goes forward")
                
            elif event.stick == RIGHT:
                r_thumb_stick_pos = (int(round(controller.r_thumb_pos[0] + 25 * event.x,0)), int(round(controller.r_thumb_pos[1] - 25 * event.y,0)))
                if r_thumb_stick_pos[0] > 200:
                    percentage_y = int(((r_thumb_stick_pos[0] - 200)/25)*100)
                    controller.comms.packetControls.packet[2] = percentage_y
                    print("Robot goes right")
                elif r_thumb_stick_pos[0] < 200:
                    percentage_y = int(((200 - r_thumb_stick_pos[0])/25)*100)
                    controller.comms.packetControls.packet[2] = percentage_y
                    print("Robot goes left")
                

        elif event.type == EVENT_TRIGGER_MOVED:
            if event.trigger == LEFT:
                l_trigger_index_pos = (controller.l_trigger_pos[0], controller.l_trigger_pos[1] - 20 + int(round(40 * event.value, 0)))
                print(l_trigger_index_pos)
                if l_trigger_index_pos[1] > 30:
                    controller.comms.packetControls.packet[7] = true
                    print("Robot goes down")
            elif event.trigger == RIGHT:
                r_trigger_index_pos = (controller.r_trigger_pos[0], controller.r_trigger_pos[1] - 20 + int(round(40 * event.value, 0)))
                print(r_trigger_index_pos)
                if r_trigger_index_pos[1] > 30:
                    controller.comms.packetControls.packet[6] = true
                    print("Robot goes up")
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
                controller.comms.packetControls.packet[5] = true
                print("Claw grabs")
            elif event.button == "B":
                controller.comms.packetControls.packet[5] = false
                print("Claw releases")                
            elif event.button == "X":
                print("Take picture")
            elif event.button == "Y":
                controller.comms.packetControls.packet[7] = true
                print("Robot is killed")
                

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
                controller.comms.packetControls.packet[5] = true
                print("Claw keeps grabbing")
            elif event.button == "B":
                controller.comms.packetControl.packet[5] = false
                print("Claw has been released")
                
            elif event.button == "X":
                print("Stop taking pictures")

            elif event.button == "Y":
                controller.comms.packetControls.packet[7] = true
                print("Robot is killed")
        
   

