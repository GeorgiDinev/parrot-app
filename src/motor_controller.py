import time
from step_motor import StepMotor

#motor_state = 'idle'
def __pull_curtain_up(step_motor, wait_seconds_before_pull):
    start_time = time.time()
    # wait x seconds before pulling the  curtain up
    while (time.time() - start_time) < wait_seconds_before_pull:
        time.sleep(1)
        print("waiting...", time.time()-start_time)

    # time has passed, its time to poll
    with open("curtain_state.txt", 'r+') as curtain_file:
        curtain_data = curtain_file.read().splitlines()
        print('curtain data:', curtain_data)
        if(curtain_data[1].strip().lower() == 'down' and curtain_data[0].strip().lower() == 'idle'):
            print('Moving up the curtain!!??')
            step_motor.setup_pins()
            step_motor.move_reverse_clockwise()# move up
            curtain_file.seek(0)
            curtain_file.write("idle\nup")
            curtain_file.truncate()

def start():
    step_motor = StepMotor([27,22,23,24], 19.5)

    step_motor.setup_pins()

    with open('curtain_state.txt', 'w') as file:
        file.seek(0)
        file.write('moving\ndown')
        file.truncate()
    step_motor.move_clockwise()#down
    with open('curtain_state.txt', 'w') as file:
        file.seek(0)
        file.write('idle\ndown')
        file.truncate()

    wait_secs_until_pull_curtain= (5 * 60) + 19.5
    __pull_curtain_up(step_motor, wait_secs_until_pull_curtain)
