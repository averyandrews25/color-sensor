import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

WAIT = 0.1

class Sensor:
    def __init__(self, pin, power):
        self.pin = pin
        GPIO.setup(pin, GPIO.IN)
        self.power = power
        GPIO.setup(self.power, GPIO.OUT)

    def time_to_full(self, count=5, average='a'):
        self.times = list(range(count))

        t = time.time()
        for i in range(count):
            GPIO.output(self.power, GPIO.LOW)
            time.sleep(WAIT)
            GPIO.output(self.power, GPIO.HIGH)

            while GPIO.input(self.pin) == GPIO.LOW:
                pass
            
            delta = time.time() - t
            self.times[i] = delta - WAIT
            t += delta

        if average == 'a':
            return sum(self.times) / len(self.times)
        elif average == 'm':
            self.times.sort()
            return self.times[len(self.times)/2]

class LED:
    def __init__(self, pin):
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        self.pin = pin
    def power(self, toggle):
        if toggle:
            GPIO.output(self.pin, GPIO.HIGH)
        else:
            GPIO.output(self.pin, GPIO.LOW)

def get_times(sensor=Sensor(38, 40), leds=[LED(pin) for pin in (11, 13, 15)]):
    vals = []
    for led in leds:
        led.power(1)
        vals.append(sensor.time_to_full())
        led.power(0)

    vals.append(sensor.time_to_full())

    return vals

if __name__ == "__main__":
    print(get_color())
    GPIO.cleanup()

