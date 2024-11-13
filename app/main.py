from buzzer import Buzzer
from sensors import Sensors
from camera import Camera

# GPIO mode is set to BCM, because of adafruit_dht library
# What? https://raspi.tv/2013/rpi-gpio-basics-4-setting-up-rpi-gpio-numbering-systems-and-inputs

# Init buzzer
b = Buzzer()
b.buzz_x_times(1)

# Init sensors
s = Sensors()
print(f"DHT11: {s.read_temp_humid()}")
print(f"Soil sensor: {s.read_soil_humid()}")

# Init camera
c = Camera()
print(f"Yellow percentage: {c.get_percentage()}")

# Clean GPIO before exit
GPIO.cleanup()