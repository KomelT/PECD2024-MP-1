from adafruit_dht import DHT11
from logs import log_event

class Sensors:
  def __init__(self, temp_humid_pin):
    self.temp_humid_pin = temp_humid_pin
    
    self.temp_humid = DHT11(temp_humid_pin)
    
  def read_temp_humid(self):
    for i in range(10):
      try:
        res = self.temp_humid
        return (res.temperature, res.humidity)
      except RuntimeError as e:
        log_event(f"[ERROR] While reading temp and humidity: {e}")
        continue