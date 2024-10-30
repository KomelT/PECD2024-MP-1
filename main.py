from buzzer import *
from sensors import *

# GPIO mode is set to BCM, because of adafruit_dht library
# What? https://raspi.tv/2013/rpi-gpio-basics-4-setting-up-rpi-gpio-numbering-systems-and-inputs

# Init buzzer
b = Buzzer()
b.buzz_x_times(2)

# Init sensors
s = Sensors()
print(s.read_temp_humid())

# Clean GPIO before exit
GPIO.cleanup()
