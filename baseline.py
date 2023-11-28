import sensor
import json
from statistics import median
import RPi.GPIO as GPIO
import numpy as np

def times_to_ratios(times):
    with open("colors.json", "r") as blinef:
        blines = json.load(blinef)
    nbase = blines["none"]
    colorb = list(blines.values())[0:3]
    return [(nbase-time)/(nbase-base) for time, base in zip(times, colorb)]

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)

    RUNS = 100

    stats = np.zeros((RUNS, 4))

    for i in range(RUNS):
        stats[i] = sensor.get_times()

    blines = {
        "red": median(stats[:,0]),
        "green": median(stats[:,1]),
        "blue": median(stats[:,2]),
        "none": median(stats[:,3])
    }

    with open("colors.json", "w") as blinef:
        blinef.write(json.dumps(blines))

    GPIO.cleanup()
