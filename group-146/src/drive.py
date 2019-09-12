import ev3dev.ev3 as ev3
import time
import const
import motors
import sensor
import odometry
from Planet import Direction, Planet


"""need: functions set_motor and get_brightness
         put robot in drive direction"""


def follow_line():
    integral = 0
    last_light_value = 0
    start_point = [odometry.rough_x_pos, odometry.rough_y_pos, odometry.get_direction_NESW()]
    motors.start_motors()
    motors.set_motor(const.MAX_SPEED / 2, const.MAX_SPEED / 2)
    while sensor.get_color():
        time.sleep(const.DELAY_START)
    time.sleep(const.DELAY_START * 10)
    # i = 0
    # timer = time.clock()
    while not sensor.get_color():
        if sensor.touch_sensor() == 1:
            motors.stop_motors()
            ev3.Sound.speak('I am waiting')
            time.sleep(const.DELAY_OBSTACLE)
            motors.start_motors()
        light_value = sensor.get_brightness()
        integral = 1/2 * integral + light_value
        derivative = light_value - last_light_value
        turn = const.KP * light_value + const.KI * integral + const.KD * derivative
        right_speed = const.AVERAGE_SPEED + turn
        left_speed = const.AVERAGE_SPEED - turn
        motors.set_motor(left_speed, right_speed)
        last_light_value = light_value
        odometry.update_direction()
        odometry.update_position()
        # i += 1
    # print("It took {}s per loop".format((time.clock()-timer)/i))
    motors.stop_motors()
    time.sleep(const.DELAY_MOTOR_SLEEP)
    motors.drive_on_point()
    time.sleep(const.DELAY_MOTOR_SLEEP)
    odometry.update_planet(0)
    end_dir = odometry.get_direction_NESW()
    if end_dir == Direction.North:
        end_dir = Direction.South
    elif end_dir == Direction.East:
        end_dir = Direction.West
    elif end_dir == Direction.South:
        end_dir = Direction.North
    else:
        end_dir = Direction.East
    end_point = [odometry.rough_x_pos, odometry.rough_y_pos, end_dir]
    print("Adding Path from {} to {}...".format(start_point, end_point))
    odometry.planet.add_path(start_point, end_point)


# sucht nach Moeglichkeiten, weiter zu fahren
# ausserdem die node zum Planeten hinzugefuegt (passiert in update_planet())
def search_for_line():
    line_direction = {Direction.North: False, Direction.East: False, Direction.South: False, Direction.West: False}
    motors.start_motors()
    motors.set_motor(const.ROTATION_SPEED, const.ROTATION_SPEED)
    while sensor.get_color():
        time.sleep(const.DELAY_START * 2)
    time.sleep(const.DELAY_DRIVE_OFF_POINT)
    motors.stop_motors()
    i = 0
    while True:
        time.sleep(const.DELAY_MOTOR_SLEEP)
        line_direction[odometry.get_direction_NESW()] = motors.turn(90)
        odometry.update_direction()
        # print(odometry.get_direction())
        i += 1
        if i == 4:
            odometry.update_planet(line_direction)
            return line_direction


def turn_direction(dir):
    while odometry.get_direction_NESW() != dir:
        motors.turn(90)


def get_direction_to_drive():
    line_direction = search_for_line()

    node = {"x_position": odometry.rough_x_pos, "y_position": odometry.rough_y_pos,
            Direction.North: line_direction[Direction.North], Direction.East: line_direction[Direction.East],
            Direction.South: line_direction[Direction.South], Direction.West: line_direction[Direction.West]}
    return odometry.planet.choose_drive_direction(node)
