import time
import time
import RPi.GPIO as GPIO
import sys

class StepMotor:
    STATE_IDLE = 1
    STATE_TRANSITION = 2
    
    def __init__(self, pin_numbers_arr, work_time_sec = 19.5):
        self.pins = pin_numbers_arr
        self.setup_pins()
        self.sequence = [ [1,0,0,0],
                [1,1,0,0],
                [0,1,0,0],
                [0,1,1,0],
                [0,0,1,0],
                [0,0,1,1],
                [0,0,0,1],
                [1,0,0,1] ]
        self.work_time_sec = work_time_sec
        self.currentState = StepMotor.STATE_IDLE

    def setup_pins(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin,False) 

    def get_state(self):
        return self.currentState

    def move_reverse_clockwise(self):
        self.__move_motor(range(7, -1, -1),range(3, -1, -1) )

    def move_clockwise(self):
        self.__move_motor(range(8),range(4))

    def __move_motor(self, half_steps_range, pins_range):
        self.currentState = StepMotor.STATE_TRANSITION
        start_time = time.time()
        while True:
            stop_motor =False
            for half_step in half_steps_range:
                for pin in pins_range:
                    GPIO.output(self.pins[pin], self.sequence[half_step][pin])
                
                curr_time = time.time()
                if (curr_time - start_time) > self.work_time_sec:
                    stop_motor = True
                    break
                time.sleep(0.0007)# min time needed for the step-motor to move
            if stop_motor:
                break
        self.currentState = StepMotor.STATE_IDLE
        GPIO.cleanup()
