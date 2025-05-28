# -- CONFIGURABLE PARAMETERS -- #

TOP_SPEED = 12
ACCELARATION = 12
TURN_SPEED = 5
SENSOR_RANGE = 1

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

    if sensors["size"] == 25:
        front = sensors["front"]
        left = sensors["left"]
        right = sensors["right"]

        safe_distance = 110

        # Acceleration logic
        accelerate = front > safe_distance or speed < 20
        brake = front < safe_distance and speed > 50  # emergency stop

        # Turning logic
        e = 2.718
        scale = 1 / (1 + e ** (-abs(speed)))
        turn = 2 / (1 + e ** (scale * (left - right))) - 1

        response = {
            "throttle": int(accelerate) - int(brake),
            "steering": round(turn, 2),
        }
        return response

    front = sensors["front"]
    left = sensors["left"]
    right = sensors["right"]

    safe_distance = 50

    # Acceleration logic
    accelerate = front > safe_distance or speed < 20
    brake = front < safe_distance and speed > 50  # emergency stop
    throttle = int(accelerate) - int(brake)

    # Turning logic
    e = 2.718
    sens = 5.5
    scale = sens * (1 / (1 + e ** (-abs(speed) / 20)) - 0.5)
    # scale = sens * abs(speed)
    scale /= front / safe_distance if front > 0 else 1
    turn = 2 / (1 + e ** (min(5, scale * (left - right)))) - 1

    if speed > 20 and speed < 150 and abs(turn) > 0.98 and front > safe_distance:
        turn /= 6

    if front < safe_distance:

        turn = (right - left) / abs(right - left) if (right != left) else 0
        if speed > 100:
            throttle = -1
        elif speed > 50:
            throttle = 0
        else:
            throttle = 1
        # print("Throttle", throttle)

    response = {
        "throttle": throttle,
        "steering": turn,
    }
    return response
