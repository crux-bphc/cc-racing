# -- CONFIGURABLE PARAMETERS -- #

TOP_SPEED = 6.5  # 7
ACCELARATION = 8  # 7
TURN_SPEED = 15.5  # 16
SENSOR_RANGE = 0

# -- THESE MUST SUM UP TO 30 ---- #

# -- AI LOGIC -- #


def ai_step(sensors, speed):
    left, right = sensors["left"], sensors["right"]

    P = 40 if sensors["size"] == 20 else 50

    turn = 0

    if right < P:
        turn = -1
    elif left < P:
        turn = 1

    if speed < 0:
        turn = 0

    response = {
        "throttle": 1,
        "steering": turn,
    }
    return response
