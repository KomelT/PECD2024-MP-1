from state import State
from parser import Parser
from buzzer import Buzzer
from sensors import Sensors
from camera import Camera
from RPi import GPIO
from time import sleep
from logs import *
# GPIO mode is set to BCM, because of adafruit_dht library
# What? https://raspi.tv/2013/rpi-gpio-basics-4-setting-up-rpi-gpio-numbering-systems-and-inputs

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

#Init Buzzer
buzzer = Buzzer()

s = Sensors()

# buzz once if the air humidit
# will buzz twice if air temperature 
# and will buzz three times in case the soil humidity drops 
air_temp, air_humid = s.read_temp_humid()
soil_humid = s.read_soil_humid()
air_temp_out_range = False
soil_humid_out_range = False

if not parser.in_range_air_humid(air_humid):
    buzzer.buzz_x_times(1)
    sleep(1)
    
if not parser.in_range_air_temp(air_temp):
    air_temp_out_range = True
    buzzer.buzz_x_times(2)
    sleep(1)
    
if not parser.in_range_soil_humid(soil_humid):
    soil_humid_out_range = True
    buzzer.buzz_x_times(3)   
    
if (air_temp_out_range or soil_humid_out_range):
    # Init Camera
    cam = Camera(sever_address="http://trojan:5000/process")
    percentage = cam.get_percentage()
    yellow_percentage = percentage['yellow_percentage'] 
    black_percentage = percentage['black_percentage'] 
    log_event(f"camera has taken a pic: black={black_percentage}% , yellow={yellow_percentage}%")
    
    if (state.waking_up):
        state.set_plant_yellow_black_percentage(yellow_percentage,black_percentage)
    else:
        if (yellow_percentage > (state.yellow_percentage+THRESHOLD)):
            buzzer.buzz_x_times(4)
        if (black_percentage > (state.black_percentage+THRESHOLD)):
            buzzer.buzz_x_times(5)   
            
# Clean GPIO before exit
GPIO.cleanup()

state.dump_state()
state.halt()