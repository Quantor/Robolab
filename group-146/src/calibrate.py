import ev3dev.ev3 as ev3
import time
import const
import sensor
import motors

btn = ev3.Button()


def calibrate_black_white():
    const.BLACK_VALUE = sensor.get_raw_brightness()
    print("Black initialized as {}!".format(const.BLACK_VALUE))
    motors.start_motors()
    motors.set_motor(const.ROTATION_SPEED, -const.ROTATION_SPEED)
    time.sleep(1)
    motors.stop_motors()
    const.WHITE_VALUE = sensor.get_raw_brightness()
    print("White initialized as {}!".format(const.WHITE_VALUE))
    motors.start_motors()
    motors.set_motor(-const.ROTATION_SPEED, const.ROTATION_SPEED)
    time.sleep(1)
    motors.stop_motors()
    time.sleep(const.DELAY_MOTOR_SLEEP)
    const.KP = const.MAX_SPEED / const.WHITE_VALUE * 0.75 * 0.6
    const.KI = 2 * const.KP * const.DT / const.PC
    const.KD = const.KP * const.PC / (8 * const.DT)


def calibrate_light_values():
    print("Now please show me red and press a button")
    while btn.any() is False:
        time.sleep(0.01)
    const.RED = sensor.get_raw_color()
    print("Thanks, red initialized as {}!".format(const.RED))
    time.sleep(0.5)
    print("Now please show me blue and press a button")
    while btn.any() is False:
        time.sleep(0.01)
    const.BLUE = sensor.get_raw_color()
    print("Thanks, blue initialized as {}!".format(const.BLUE))
    time.sleep(0.5)
    print("Starting in ")
    for i in range(10, 0, -1):
        print("{}...".format(i))
        time.sleep(1)