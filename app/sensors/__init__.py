from adafruit_dht import DHT11
from logs import log_event
from board import D4
from gpiozero import MCP3008


class Sensors:
    def __init__(self, temp_humid_pin=D4, soil_humid_cs_pin=0):
        # Temperature and humidity sensor
        self.temp_humid_pin = temp_humid_pin
        self.temp_humid = DHT11(temp_humid_pin)

        # Soil humidity sensor
        self.soil_humid = MCP3008(soil_humid_cs_pin)

    def read_temp_humid(self):
        for i in range(10):
            try:
                res = self.temp_humid
                log_event(f"air_temp = {res.temperature}")
                log_event(f"air_humid = {res.humidity}")
                return (res.temperature, res.humidity)
            except RuntimeError as e:
                log_event(f"[ERROR] While reading temp and humidity: {e}")
                continue

    def read_soil_humid(self):
        try:
            percentage = round(self.soil_humid.value * 100, 2)
            log_event(f"soil_humid = {percentage}")
            return percentage
        except RuntimeError as e:
            log_event(f"[ERROR] While reading soil humidity: {e}")
            return None
