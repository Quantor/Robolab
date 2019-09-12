import ev3dev.ev3 as ev3
import drive
import motors
import sensor
import time
import odometry
import calibrate
from Planet import Direction, Planet


def run():
    sensor.init_color_sensor()
    motors.init_motors()
    odometry.init_odometry()
    while calibrate.btn.any() is False:
        time.sleep(0.001)
    explore()
    '''
    # the execution of all code shall be started from within this function
    print("Hello World!")
    drive.follow_line()
    line_direction = drive.search_for_line()
    print(line_direction)
    motors.stop_motors()
    '''


def explore():
    while True:
        drive.follow_line()
        direction_to_drive = drive.get_direction_to_drive()
        print("Driving to the {}".format(direction_to_drive))
        drive.turn_direction(direction_to_drive)


def test_brightness():
    while True:
        print(sensor.get_raw_brightness())
        while calibrate.btn.any() is False:
            pass
        time.sleep(0.5)


def test_motor_rotation():
    i = 0
    motors.set_motor(20, 0)
    while i < 40:
        print(motors.get_motor_rotation())
        time.sleep(0.2)
        i = i + 1
    motors.stop_motors()


if __name__ == '__main__':
    run()
