# https://youtu.be/vFJl-00C_bw - truly the greatest driver of all time
import math
# -- CONFIGURABLE PARAMETERS -- #

TOP_SPEED = 9       # times 10 + 100
ACCELARATION = 8.5    # times 5 + 10
#    ^
TURN_SPEED = 9.5      # times 5 + 100
SENSOR_RANGE = 2   # times 12 + 100

# -- THESE MUST SUM UP TO 30 ---- #

# -- AI LOGIC -- #

# who needs consys, when you can just try writing this function to understand
# why we don't use open loop systems
def ai_step(sensors, speed):
    maxspeed = 100 + TOP_SPEED * 10
    accn = 10 + ACCELARATION * 5
    turnrate = 100 + TURN_SPEED * 5
    maxsensor = 100 + SENSOR_RANGE * 12
    dt = 0.016
    FPS = 60
    """
    Sensors: dict with keys 'front', 'left', 'right'
    Values are distances (larger = more space).

    Returns a dictionary with "throttle" and "steering" values.
    Throttle is from -1 (full reverse) to 1 (full accelerate).
    Steering is from -1 (full left) to 1 (full right).
    """

    stopping_distance = (speed * speed) / (2 * accn)
    #circle_time = 360 / (turnrate * dt * FPS)
    #turning_radius = (speed * circle_time) / (2 * 3.14159)

    front = sensors["front"]
    left = sensors["left"]
    right = sensors["right"]

    throttle = 0
    steering = 0

    # treat front, right, left as vectors and add
    lateral_axis = (right - left) * 1.41421356237
    main_axis = front + lateral_axis

    if stopping_distance > front:
        throtttle = -1
    else:
        throttle = 1

    req_angle = math.degrees(math.atan(lateral_axis / main_axis))
    steering = (req_angle / (turnrate * dt))
    steering = max(-1, min(steering, 0.8)) * speed / maxspeed

    #print(turnrate * dt)
    #print("Steering:", req_angle, steering)
    #print("Throttle:", throttle)
    
    if front >= maxsensor and left > 30 and right > 30:
        throttle = 1

        # attempt to center
        steering = (right - left) / maxsensor
        # print("Straight mode")

    if front < 65 or speed < 0:
        # print("EMERGENCY FRONT MODE")
        throttle = 0.1
        if right > left:
            steering = 1
        else:
            steering = -1
        if speed < 0:
            throttle = 1

    if left < 25:
        # print("EMERGENCY SIDE MODE left")
        steering = 1
    if right < 25:
        # print("EMERGENCY SIDE MODE right")
        steering = -1

    t = max(-1, min(throttle, 1))
    s = max(-1, min(steering, 1))
    response = {
        "throttle": t,
        "steering": s,
    }
    # print(t, s)
    return response
