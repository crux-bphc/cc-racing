# -- CONFIGURABLE PARAMETERS -- #

TOP_SPEED = 10
ACCELARATION = 4
TURN_SPEED = 7
SENSOR_RANGE = 9

# -- THESE MUST SUM UP TO 30 ---- #

# -- AI LOGIC -- #


import random

# Global state
recovery_state = {"zigzag_mode": False, "zigzag_timer": 0, "zigzag_dir": 1}


def ai_step(sensors, speed):
    front = sensors["front"]
    left = sensors["left"]
    right = sensors["right"]

    # print(f"AI Sensors: Front={front}, Left={left}, Right={right}, Speed={speed}")

    # Parameters
    safe_distance = 110
    turn_detect_distance = 85
    stuck_threshold = 57
    stuck_speed = 10
    max_safe_speed_in_turn = 70
    approaching_turn_distance = 180

    throttle = 0
    turn = 0

    # === Stuck Detection ===
    if left < stuck_threshold and right < stuck_threshold and speed < stuck_speed:
        recovery_state["zigzag_mode"] = True
        recovery_state["zigzag_timer"] = 0
        recovery_state["zigzag_dir"] = random.choice([-1, 1])

    # === Zigzag Recovery Mode ===
    if recovery_state["zigzag_mode"]:
        recovery_state["zigzag_timer"] += 1

        # Zigzag every 10 frames
        if recovery_state["zigzag_timer"] % 10 == 0:
            recovery_state["zigzag_dir"] *= -1  # alternate direction

        turn = recovery_state["zigzag_dir"]
        throttle = 1

        # Exit zigzag if recovered
        if speed > 20 or abs(left - right) < 10:
            recovery_state["zigzag_mode"] = False
            recovery_state["zigzag_timer"] = 0

        return {"throttle": round(throttle, 2), "steering": round(turn, 2)}

    # === Normal Driving ===
    # Delay turn until front is small, and one side opens up
    if front < 150:
        if left > right + 30:
            turn = -0.7  # turn left
        elif right > left + 30:
            turn = 0.7  # turn right
    else:
        # Straighten
        if left > right:
            turn = -0.3 * (1 - right / (left + 0.01))
        elif right > left:
            turn = 0.3 * (1 - left / (right + 0.01))

    # Throttle logic
    if front > safe_distance:
        throttle = 1
    elif speed > max_safe_speed_in_turn and front < approaching_turn_distance:
        throttle = -1  # brake before sharp bend
    else:
        throttle = 0.3

    return {"throttle": round(throttle, 2), "steering": round(turn, 2)}
