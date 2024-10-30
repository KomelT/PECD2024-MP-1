from adafruit_dht import DHT11
from logs import log_event
from time import sleep
import busio
import digitalio
from board import D5, D4, SCK, MISO, MOSI
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


class Sensors:
    def __init__(self, temp_humid_pin=D4, soil_humid_cs_pin=D5):
        # Temperature and humidity sensor
        self.temp_humid_pin = temp_humid_pin
        self.temp_humid = DHT11(temp_humid_pin)

        # Soil humidity sensor
        spi = busio.SPI(clock=SCK, MISO=MISO, MOSI=MOSI)
        cs = digitalio.DigitalInOut(soil_humid_cs_pin)
        self.mcp = MCP.MCP3008(spi, cs)

    def read_temp_humid(self):
        for i in range(10):
            try:
                res = self.temp_humid
                return (res.temperature, res.humidity)
            except RuntimeError as e:
                log_event(f"[ERROR] While reading temp and humidity: {e}")
                continue

    def read_soil_humid(self):
        channel = AnalogIn(self.mcp, MCP.P0)
        print("Raw ADC Value: ", channel.value)
        print("ADC Voltage: " + str(channel.voltage) + "V")
