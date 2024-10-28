from parser import *
from sensors import *
from time import sleep
import board

# Read configuration file
c = Parser()
c.read_conf()
c.print_range_values()


# Config sensors
s = Sensors(board.D14)

while True:
  print(s.read_temp_humid())
  sleep(1)