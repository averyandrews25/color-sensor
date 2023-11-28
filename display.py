import RPi.GPIO as GPIO
import baseline
import sensor
import time

RRATE = 75

times = sensor.get_times()
color = baseline.times_to_ratios(times)

for i, r in enumerate(color):
    color[i] = r**20
    if r > 1:
        color[i] = 1

percents = []
if sum(color) < 0.7:
    print("less than .7")
    percents = [(r**0.6)*100 for r in color]
else:
    percents = [r*100 for r in color]

print(color)

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

leds = []

for pin in (18, 23, 24):
    GPIO.setup(pin, GPIO.OUT)
    leds.append(GPIO.PWM(pin, RRATE))

for led, val in zip(leds, percents):
    led.start(0)
    led.ChangeDutyCycle(val)

time.sleep(5)

GPIO.cleanup()
