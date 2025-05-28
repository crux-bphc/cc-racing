# -- CONFIGURABLE PARAMETERS -- #

TOP_SPEED = 11
ACCELARATION = 9
TURN_SPEED = 8
SENSOR_RANGE = 2

# -- THESE MUST SUM UP TO 30 ---- #

# -- AI LOGIC -- #

def classify_range(value, min_range, mid_range, max_range):
    if value >= max_range:
        return 3
    elif value >= mid_range:
        return 2
    elif value >= min_range:
        return 1
    else:
        return 0

def ai_step(sensors, speed):
    """
    Sensors: dict with keys 'front', 'left', 'right'
    Values are distances (larger = more space).

    Returns a dictionary with "throttle" and "steering" values.
    Throttle is from -1 (full reverse) to 1 (full accelerate).
    Steering is from -1 (full left) to 1 (full right).
    """
    front = sensors["front"]
    left = sensors["left"]
    right = sensors["right"]
    size = sensors["right"]

    throttle_list = [
    [[-1.0, -0.5, -0.5, -0.5],
    [0.8, 0.8, 0.8, 0.8],
    [0.8, 0.8, 0.8, 1.0],
    [0.8, 0.8, 0.8, 1.0]],

    [[-0.5, 0.5, 0.8, 0.8],
    [0.8, 0.8, 0.8, 0.8],
    [0.8, 0.8, 0.8, 1.0],
    [0.8, 0.8, 1.0, 1.0]],

    [[-0.5, 0.8, 0.8, 0.8],
    [0.8, 0.8, 0.8, 1.0],
    [0.8, 0.8, 1.0, 1.0],
    [0.8, 1.0, 1.0, 1.0]],

    [[-0.5, 0.8, 0.8, 1.0],
    [0.8, 0.8, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0]]
    ]



    steer_mul_list = [[[1.0, 0.9, 0.8, 0.8],
            [1.0, 0.8, 0.8, 0.5],
            [0.9, 0.8, 0.8, 0.5],
            [0.8, 0.8, 0.8, 0.5]],
            [[0.9, 0.9, 0.8, 0.5],
            [0.8, 0.8, 0.5, 0.3],
            [0.8, 0.8, 0.5, 0.3],
            [0.8, 0.5, 0.5, 0.3]],
            [[0.8, 0.8, 0.8, 0.5],
            [0.8, 0.5, 0.5, 0.3],
            [0.8, 0.5, 0.5, 0.3],
            [0.8, 0.5, 0.5, 0.0]],
            [[0.8, 0.5, 0.5, 0.5],
            [0.5, 0.3, 0.3, 0.3],
            [0.5, 0.3, 0.3, 0.3],
            [0.5, 0.3, 0.0, 0.0]]]

    max_range = (SENSOR_RANGE * 12) + 100
    min_range = 80
    mid_range = (max_range + min_range) / 2 + 10

    l = classify_range(left, min_range, mid_range, max_range)
    f = classify_range(front, min_range, mid_range, max_range)
    r = classify_range(right, min_range, mid_range, max_range)

    base_steer = ((right-left) / max(right, left))
    
    throttle = 2 * (throttle_list[l][f][r])
    steering = 2.73 * base_steer * steer_mul_list[l][f][r]

    throttle = max(-1, min(1, throttle))
    steering = max(-1, min(1, steering))

    if 0 < speed < 50 and throttle < 0:
        throttle *= -1

    response = {
        "throttle": throttle,
        "steering": steering,
    }
    return response
