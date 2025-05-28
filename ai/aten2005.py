# -- CONFIGURABLE PARAMETERS -- #

TOP_SPEED = 10
ACCELARATION = 11
TURN_SPEED = 7
SENSOR_RANGE = 2

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

    safe_distance = 80
    safe_turn_distance = 10

    max_speed = TOP_SPEED * 10 + 100

    # Acceleration logic
    accelerate = front > safe_distance or speed < 20
    brake = front < safe_distance and speed > 50  # emergency stop

    throttle = int(accelerate) - int(brake)

    turn_multiplier = 1.2 * (sensors["size"] / 20)
    speed_multiplier = 1

    if (left / right > 1.7 or right / left > 1.7) and speed > 130:
        # throttle = -.5
        turn_multiplier = 2

    if speed > max_speed - 60:
        speed_multiplier = speed / (100 + TOP_SPEED * 10) * 1.5

    turn = ((right - left) / (left + right)) * turn_multiplier

    THRESH = 90

    if (left > THRESH or right > THRESH) and speed > max_speed - 20:
        turn *= 100
        turn = max(-0.85, min(0.85, turn))

    if left < safe_turn_distance or right < safe_turn_distance:
        turn *= -1

    if speed < max_speed - 50:
        throttle = 1

    response = {
        "throttle": throttle,
        "steering": round(turn, 2),
    }

    return response
