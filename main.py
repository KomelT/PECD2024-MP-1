from parser import *
from sensors import *
from time import sleep
from board import D14

# Read configuration file
c = Parser()
c.read_conf()

# Config sensors
s = Sensors(D14)


s.read_soil_humid()