# -- CONFIGURABLE PARAMETERS -- #

TOP_SPEED = 12
ACCELARATION = 10
TURN_SPEED = 8
SENSOR_RANGE = 0

# -- THESE MUST SUM UP TO 30 ---- #

# -- AI LOGIC -- #


### Proportional controller by Bipul. P.S. consys actually might have been a lil bit useful haha
class PController:
    def __init__(self, Kp):
        self.Kp = Kp

    def update(self, error):
        return self.Kp * error


steering_p = PController(Kp=0.035)
speed_p = PController(Kp=0.1)

TARGET_SPEED = 230


def ai_step(sensors, speed):
    """
    sensors: {'front': d, 'left': d, 'right': d}, where left/right are at ±45 degrees.
    """

    steering_error = sensors["right"] - sensors["left"]
    steering_output = steering_p.update(steering_error)
    steering = max(-1, min(1, steering_output))

    if sensors["front"] < 80:
        speed_error = -20  # -10 is good
    else:
        speed_error = TARGET_SPEED - speed

    throttle_output = speed_p.update(speed_error)
    throttle = max(-1, min(1, throttle_output))

    return {"throttle": round(throttle, 2), "steering": round(steering, 2)}
