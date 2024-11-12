from time import sleep
import RPi.GPIO as GPIO
from logs import log_event


class Buzzer:
    def __init__(self, pin=18):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 10)
        self.pwm.start(0)

    def buzz(self, duration=1):
        self.pwm.ChangeFrequency(1500)
        self.pwm.ChangeDutyCycle(100)
        sleep(duration)
        self.pwm.ChangeDutyCycle(0)

    def buzz_x_times(self, times=1):
        log_event(f"buzzer {times}")
        for i in range(times):
            self.buzz()
            sleep(0.5)
