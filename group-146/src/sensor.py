import ev3dev.ev3 as ev3
import const
import colorsys

cs = 0


def init_color_sensor():
    global cs
    cs = ev3.ColorSensor(const.COLORPORT)
    cs.mode = 'RGB-RAW'


def get_raw_brightness():
    global cs
    var = cs.bin_data("hhh")
    h = var[0]/255.0/3
    s = var[1]/255.0/3
    v = var[2]/255.0/3
    greyscaled = colorsys.rgb_to_hsv(h, s, v)
    return greyscaled[2]


def get_brightness():
    return get_raw_brightness()-const.BLACK_VALUE-(const.WHITE_VALUE-const.BLACK_VALUE)/2


def get_raw_color():
    global cs
    var = cs.bin_data("hhh")
    col = (var[0] / 255, var[1] / 255, var[2] / 255)
    return col


def get_color():
    global cs
    color = get_raw_color()
    # print(color)
    is_red = True
    for i in range(0, 3):
        if (1 - const.TOLERANCE) * const.RED[i] < color[i] < (1 + const.TOLERANCE) * const.RED[i]:
            # wenn die gemessene Farbe innerhalb der Toleranz liegt ist alles ok
            pass
        else:
            # ansonsten nicht
            is_red = False
            break
    if is_red is True:
        print("Rot gefunden")
        return True
    is_blue = True
    for i in range(0, 3):
        if (1 - const.TOLERANCE) * const.BLUE[i] < color[i] < (1 + const.TOLERANCE) * const.BLUE[i]:
            # wenn die gemessene Farbe innerhalb der Toleranz liegt ist alles ok
            pass
        else:
            # ansonsten nicht
            is_blue = False
            break
    if is_blue is True:
        print("Blau gefunden")
        return True
    # wenn keine Farbe erkannt wurde
    return False


def touch_sensor():
    ts1 = ev3.TouchSensor(const.TOUCH1PORT)
    ts2 = ev3.TouchSensor(const.TOUCH2PORT)
    # print(ts1.value(), ts2.value())
    if ts1.value() is 1 or ts2.value() is 1:
        return 1
    else:
        return 0
