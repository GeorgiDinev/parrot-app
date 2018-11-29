from step_motor import StepMotor
from threading import Thread
import time
from subprocess import call
import motor_controller

class StepMotorManager:
    def __init__(self):
        self.reset_remaining_time = True

    def onParrotScream(self):
        # check if the motor is idle and the curtain is up -> move the curtain down
        with open('curtain_state.txt', 'r+') as curtain_file:
            curtain_data = curtain_file.read().splitlines()
            moving_state = curtain_data[0]

            if moving_state.strip().lower() == 'moving': return
            if(curtain_data[1].strip().lower() == 'up'):
                thread = Thread(target= motor_controller.start)
                thread.start()
