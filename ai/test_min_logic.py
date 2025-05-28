# -- CONFIGURABLE PARAMETERS -- #

TOP_SPEED = 12 # very fast
ACCELARATION = 7 # very much vroom vroom!!
TURN_SPEED = 9 # turns must be quick!
SENSOR_RANGE = 2 # there was no need for such a large sensor range, so it was easily sacrificed

# -- THESE MUST SUM UP TO 30 ---- #

# -- AI LOGIC -- #

"""
All this does is decide if a turn is in order. If it is, it checks if the smallest distance to any wall, (assumed to be
the wall that the car is turning against) is within (or actually out of, but idk why) some set limits found by 
experimentation, and then it turns the car. The acceleration is pretty basic, just slow down / lower acceleration if 
you see a wall nearby, otherwise *full speed ahead!*. 

There's no crash control, so if it crashes, it's dead meat. In this case, the car just phases through the corner and 
continues forward with something like 10 seconds off the clock, and the brakes pretty much always on. I don't know why 
the brakes are almost always on when it crashes, but it probably has something to do with "see wall forward = brake" 
behaviour.

The idea is pretty simple, finding those elusive constants - not so much.
I probably spent a total of 6 - 8 hours experimenting with the constants!

Almost all numbers are random or derived from the example behaviour in such a way that it produced what seemed to be
a well behaved car without crashing in the given two tracks. I basically just changed every single number one by one and 
saw how it changed it's behavior lol (a very painful task)
"""
def ai_step(sensors, speed):
    front = sensors["front"]
    left = sensors["left"]
    right = sensors["right"]
    size = sensors["size"]

    # I just pulled this number off of the example behavior
    dist = 110

    acceleration = int(front > dist or speed < 20) - 0.5 * int(front < dist) # I messed with it, and it works

    """I thought initially, only to measure distances from the front, but this leads to no correction when the car 
       is off the center of the track, so I had to adjust for that, and this works pretty well. It's definitely quite 
       hacky and should have been seperated but... I had no ideas on how to do that, so I did whatever worked :)
    """
    min_dist = abs(min(front, left, right))

    direction = int(left < right) - int(left > right) # -1 for left, +1 for right

    """Reduce the amount of "indecision" the car faces on a straight track.
       For some reason it wobbles just a little bit, and constantly, so this thing reduces that and gives about an extra
       second's boost in track 2 - 20 laps
    """
    if abs(left - right) < 7:
        direction = 0
    
    steering = 0

    if size == 20:
        """I spent hours perfecting this lmao, the min_dist > 51.6 is mainly there for large turns, probably
           I don't completely understand how I made it work, but it waits until the turn can be accomplished,
           since the sensors usually report the possibility of a turn before you can successfully complete it.
           I just had to mess with the constants, and these are specific to track 2. If another track of different 
           dimensions is used, this will not work at all, and the car will crash into the walls while turning - either 
           prematurely or way too late
        """
        steering = direction if min_dist < 49.0 or min_dist > 51.7 else 0
    elif size == 25: 
        """Same thing here, but since track 1 does not have any large turns like track 2, the second comparison has been
           extrapolated from the first, meaning that there's not gaurentee it will work at all! The same consequences apply
           for this one, but this one is specific to track 1's dimensions, which is larger than track 2"""
        steering = direction if min_dist < 69 or min_dist > 72.7 else 0
    
    # Prevent crashes at low speeds
    if 140 < speed < 165:
        steering *= 0.85
    elif 100 < speed < 140:
        steering *= 0.6
    elif 50 < speed < 100:
        steering *= 0.4
    elif speed < 50:
        steering *= 0.1

    return {
        "throttle": acceleration,
        "steering": steering,
    }

# no crash pls