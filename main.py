import sensor
import baseline
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

times = sensor.get_times()

for color in baseline.times_to_ratios(times):
    print((color**2)*255)

GPIO.cleanup()
