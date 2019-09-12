import ev3dev.ev3 as ev3
import sensor
import time
import const
import Planet
import odometry

left_motor = 0
right_motor = 0
left_motor_pos_save_dist = 0
right_motor_pos_save_dist = 0


def init_motors():
    global left_motor
    global right_motor
    left_motor = ev3.LargeMotor(const.LEFTMOTORPORT)
    right_motor = ev3.LargeMotor(const.RIGHTMOTORPORT)
    left_motor.reset()
    right_motor.reset()
    left_motor.stop_action = 'brake'
    right_motor.stop_action = 'brake'


def start_motors():
    global left_motor
    global right_motor
    left_motor.command = 'run-direct'
    right_motor.command = 'run-direct'


def reset_motors():
    global left_motor
    global right_motor
    left_motor.reset()
    right_motor.reset()
    left_motor.position = 0
    right_motor.position = 0
    left_motor.stop_action = 'brake'
    right_motor.stop_action = 'brake'


def set_motor(left_speed, right_speed):
    global left_motor
    global right_motor
    left_motor.duty_cycle_sp = left_speed
    right_motor.duty_cycle_sp = right_speed


def stop_motors():
    global left_motor
    global right_motor
    left_motor.duty_cycle_sp = 0
    right_motor.duty_cycle_sp = 0
    left_motor.stop()
    right_motor.stop()


def get_motor_rotation():
    global left_motor
    global right_motor
    return left_motor.position, right_motor.position


# returns the driven distance since last call in mm
def get_dist_driven():
    global left_motor
    global right_motor
    global left_motor_pos_save_dist
    global right_motor_pos_save_dist
    dist = (left_motor.position - left_motor_pos_save_dist + right_motor.position - right_motor_pos_save_dist) / 2
    dist *= const.MM_PER_DEG
    left_motor_pos_save_dist = left_motor.position
    right_motor_pos_save_dist = right_motor.position
    return dist


def reset_dist_driven():
    global left_motor_pos_save_dist
    global right_motor_pos_save_dist
    left_motor_pos_save_dist = 0
    right_motor_pos_save_dist = 0


def get_robot_rotation():
    global left_motor
    global right_motor
    rotation = (left_motor.position - right_motor.position) * const.ROTATIONFACTOR * 0.88235294
    return rotation


def turn(degree):
    global left_motor
    global right_motor
    start_motors()
    pos_save = left_motor.position
    left_motor.position = 0
    if degree < 0:
        degree += 360
    set_motor(const.ROTATION_SPEED, -const.ROTATION_SPEED)
    limit = (degree/2)/const.ROTATIONFACTOR * 1.12
    while left_motor.position < limit:
        if left_motor.position > limit/2:       # wenn schon ueber die haelfte gedreht, ausschau nach ner Linie halten
            if sensor.get_brightness() < 0 and sensor.get_color() is False:     # wenn er schwarz sieht (und keine Ecke vom Punkt)
                # noch moeglichst bis an die rechte Kante der schwarzen Linie drehen
                time.sleep(0.2)
                while sensor.get_brightness() < -(const.WHITE_VALUE - const.BLACK_VALUE)/2:
                    time.sleep(0.01)
                stop_motors()
                time.sleep(const.DELAY_MOTOR_SLEEP)
                odometry.update_planet(0)
                left_motor.position += pos_save
                return True     # es wurde eine Linie gefunden
        time.sleep(0.001)
    stop_motors()
    time.sleep(const.DELAY_MOTOR_SLEEP)
    odometry.update_planet(0)
    left_motor.position += pos_save
    return False    # es wurde keine Linie gefunden


def drive_on_point():
    time.sleep(const.DELAY_MOTOR_SLEEP)
    start_motors()
    set_motor(0, const.ROTATION_SPEED)
    time.sleep(0.7)
    stop_motors()
    time.sleep(const.DELAY_MOTOR_SLEEP)
    start_motors()
    set_motor(const.ROTATION_SPEED, 0)
    time.sleep(0.7)
    stop_motors()
    time.sleep(const.DELAY_MOTOR_SLEEP)
