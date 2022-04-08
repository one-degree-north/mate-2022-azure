from XInput import *

set_deadzone(DEADZONE_TRIGGER,10)

class Controller():
    def __init__(self, center, comms):
        self.center = center
        self.comms = comms
        self.on_indicator_pos = (self.center[0], self.center[1] - 50)       
        self.r_thumb_pos = (self.center[0] + 50, self.center[1] + 20)
        self.l_thumb_pos = (self.center[0] - 100, self.center[1] - 20)        
        self.l_trigger_pos = (self.center[0] - 120, self.center[1] - 70)           
        self.r_trigger_pos = (self.center[0] + 120, self.center[1] - 70)             
        self.buttons_pos = (self.center[0] + 100, self.center[1] - 20)
        self.A_button_pos = (self.buttons_pos[0], self.buttons_pos[1] + 20)
        self.B_button_pos = (self.buttons_pos[0] + 20, self.buttons_pos[1])
        self.Y_button_pos = (self.buttons_pos[0], self.buttons_pos[1] - 20)
        self.X_button_pos = (self.buttons_pos[0] - 20, self.buttons_pos[1])        
        self.dpad_pos = (self.center[0] - 50, self.center[1] + 20)
        self.back_button_pos = (self.center[0] - 20, self.center[1] - 20)
        self.start_button_pos = (self.center[0] + 20, self.center[1] - 20)
        self.l_shoulder_pos = (self.center[0] - 90, self.center[1] - 70)
        self.r_shoulder_pos = (self.center[0] + 90, self.center[1] - 70)