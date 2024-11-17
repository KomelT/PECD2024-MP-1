from state import State
from parser import Parser
from buzzer import Buzzer
from sensors import Sensors
from camera import Camera
from RPi import GPIO
from time import sleep
from logs import log_event, is_daylight

# GPIO mode is set to BCM, because of adafruit_dht library
# What? https://raspi.tv/2013/rpi-gpio-basics-4-setting-up-rpi-gpio-numbering-systems-and-inputs

LOCAL_MODE = False  # Set to True if you want to do plant recognition locally
THRESHOLD = 0.9

# Init State
state = State()
if not state.halted and not state.waking_up:
    print("[INFO] Exiting because not waking from halted state")
    exit(0)

# Now the device is not halted
state.halted = False

# Init Parser
parser = Parser()
parser.read_conf()

# Init Buzzer
buzzer = Buzzer()

s = Sensors()

# buzz once if the air humidit
# will buzz twice if air temperature
# and will buzz three times in case the soil humidity drops
air_temp, air_humid = s.read_temp_humid()
soil_humid = s.read_soil_humid()

air_humid_out_range = not parser.in_range_air_humid(air_humid)
air_temp_out_range = not parser.in_range_air_temp(air_temp)
soil_humid_out_range = not parser.in_range_soil_humid(soil_humid)

if air_humid_out_range:
    buzzer.buzz_x_times(1)
    sleep(1)

if air_temp_out_range:
    buzzer.buzz_x_times(2)
    sleep(1)

if soil_humid_out_range:
    buzzer.buzz_x_times(3)

if (air_humid_out_range or air_temp_out_range or soil_humid_out_range) and (
    is_daylight()
):
    # Init Camera
    cam = Camera(sever_address="http://trojan:5000/process")
    percentage = cam.get_percentage()
    plant_yellow_percentage = percentage["plant_yellow_percentage"]
    plant_black_percentage = percentage["plant_black_percentage"]
    log_event(
        f"camera has taken a pic: black={plant_black_percentage}% , yellow={plant_yellow_percentage}%"
    )

    if state.waking_up:
        state.set_plant_yellow_plant_black_percentage(
            plant_yellow_percentage, plant_black_percentage
        )
    else:
        if plant_yellow_percentage > (state.plant_yellow_percentage + THRESHOLD):
            buzzer.buzz_x_times(4)
        if plant_black_percentage > (state.plant_black_percentage + THRESHOLD):
            buzzer.buzz_x_times(5)

# Clean GPIO before exit
GPIO.cleanup()

state.dump_state()
state.halt()
