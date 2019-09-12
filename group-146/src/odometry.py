from ev3dev.ev3 import *
import Planet
import motors
import math
import const

# rough_direction ist 0 in Richtung Norden und zaehlt sonst im Uhrzeigersinn Grad hoch
# also 90 Grad sind Osten, 180 Sueden und 270 Westen
# es enthaelt immer die letzte bekannte Richtung an einem Knoten
# Norden: y +
# Osten:  x +
# Sueden: y -
# Westen: x -
# direction selbst wird an jedem Knoten wieder auf eine Himmelsrichtung gerundet

direction = 0
rough_direction = 0     # rundet die Richtung auf eine Himmelsrichtung, wenn er einmal angekommen ist
                        # (wenn update_rough_direction() aufgerufen wird)
x_pos = 0               # das ist blos relativ zum letzten Punkt von dem er losgefahren ist.
y_pos = 0               # genauso
rough_x_pos = 0         # wie bei rough_direction wird auf einen Punkt im Grid festgelegt, wenn
rough_y_pos = 0         # update_rough_position() aufgerufen wird, z.B. am Ende von follow_line()
planet = 0              # enthaelt den ganzen Planeten, wird nach und nach in update_planet() aufgebaut


def init_odometry():
    global direction
    global planet
    planet = Planet.Planet()
    planet.__init__()
    direction = 0
    init_position(0, 0)


def init_position(x, y):
    global x_pos
    global y_pos
    x_pos = x
    y_pos = y


def update_position():
    global x_pos
    global y_pos
    dist = motors.get_dist_driven()
    dir = math.radians(get_direction())
    x_d = math.sin(dir) * dist  # * const.MM_TO_GRID
    y_d = math.cos(dir) * dist  # * const.MM_TO_GRID
    # print("Moved total of {} mm in direction {}".format(dist, dir))
    # print("Moved: in x: {} and in y: {}".format(x_d, y_d))
    x_pos += x_d
    y_pos += y_d
    # print("Current Position: x: {} y: {}".format(x_pos, y_pos))


def update_direction():
    global direction
    global rough_direction
    direction = (rough_direction + motors.get_robot_rotation()) % 360
    # print("Current Direction: {}".format(direction))


def update_rough_direction():
    global direction
    global rough_direction
    # lcd = Screen()
    # lcd.draw.rectangle((0, 0, 177, 40), fill='black')
    if 45 <= direction < 135:
        # lcd.draw.text((48, 13), 'OSTEN', fill='white')
        rough_direction = 90
    elif 135 <= direction < 225:
        # lcd.draw.text((48, 13), 'SUEDEN', fill='white')
        rough_direction = 180
    elif 225 <= direction < 315:
        # lcd.draw.text((48, 13), 'WESTEN', fill='white')
        rough_direction = 270
    else:
        # lcd.draw.text((48, 13), 'NORDEN', fill='white')
        rough_direction = 0
    rough_direction = rough_direction % 360
    direction = rough_direction


def update_rough_position():
    global x_pos
    global y_pos
    global rough_x_pos
    global rough_y_pos
    rough_x_pos += round(x_pos * const.MM_TO_GRID)
    rough_y_pos += round(y_pos * const.MM_TO_GRID)
    motors.reset_dist_driven()
    x_pos = 0
    y_pos = 0


# Die Funktion sollte aufgerufen werden, wenn ein neuer Punkt angefahren wurde
def update_planet(line_direction):
    global planet
    global rough_x_pos
    global rough_y_pos
    global rough_direction
    update_direction()
    update_rough_direction()
    update_position()
    update_rough_position()
    motors.reset_motors()   # die Motorenpositionen muessen resettet werden
    if line_direction != 0:
        planet.add_node(rough_x_pos, rough_y_pos, line_direction)
    print("X-Koordinate: {} Y-Koordinate: {} Richtung: {}".format(rough_x_pos, rough_y_pos, rough_direction))


def get_direction():
    global direction
    update_direction()
    return direction


def get_direction_NESW():
    global direction
    update_direction()
    if 45 < direction <= 135:
        return Planet.Direction.East
    if 135 < direction <= 225:
        return Planet.Direction.South
    if 225 < direction <= 315:
        return Planet.Direction.West
    return Planet.Direction.North
