# -- CONFIGURABLE PARAMETERS -- #

TOP_SPEED = 10
ACCELARATION = 4
TURN_SPEED = 7
SENSOR_RANGE = 9

# -- THESE MUST SUM UP TO 30 ---- #

# -- AI LOGIC -- #


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

    safe_distance = 110

    # Acceleration logic
    accelerate = front > safe_distance or speed < 20
    brake = front < safe_distance and speed > 50  # emergency stop

    # Turning logic
    if left > right:
        turn = -0.5 * (1 - right / (left + 0.01))
    elif right > left:
        turn = 0.5 * (1 - left / (right + 0.01))
    else:
        turn = 0

    response = {
        "throttle": int(accelerate) - int(brake),
        "steering": round(turn, 2),
    }
    return response
