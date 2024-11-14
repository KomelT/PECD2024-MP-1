from state import State
from buzzer import Buzzer
from sensors import Sensors
from camera import Camera

# GPIO mode is set to BCM, because of adafruit_dht library
# What? https://raspi.tv/2013/rpi-gpio-basics-4-setting-up-rpi-gpio-numbering-systems-and-inputs

# Init State
state = State()
if not state.halted:
    exit(0)

# Init buzzer
b = Buzzer()
b.buzz_x_times(1)

# Init sensors
s = Sensors()
print(f"DHT11: {s.read_temp_humid()}")
print(f"Soil sensor: {s.read_soil_humid()}")

# Init camera
c = Camera()
percent = c.get_percentage()
print(f"Yellow percentage: {percent['yellow_percentage']}")
print(f"Black percentage: {percent['black_percentage']}")
print(f"Green percentage: {percent['green_percentage']}")


# 1. initial sensing
# 2. once a day humidity and temp
# 3. if is more than 21 degrees -> sensing 12 hours
# 4 if humidity very low -> picture
# 5 pif


# Clean GPIO before exit
GPIO.cleanup()
