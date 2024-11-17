from os import path


class Parser:
    def __init__(self):
        print("[INFO] Parser init")
        self.min_air_humidity = 0.0
        self.min_soil_humidity = 0.0
        self.min_air_temp = 0.0

        self.max_air_humidity = 100.0
        self.max_soil_humidity = 100.0
        self.max_air_temp = 60.0

    def read_conf(self):
        basedir = path.abspath(path.dirname(__file__))
        with open(f"{basedir}/../configuration.txt", "r") as f:
            while True:
                line = f.readline()
                if line == "":
                    print("[INFO] Configuration file is read")
                    break
                line_arr = line.split(" ")

                # parsing air humidity
                if line_arr[0] == "air_humidity":
                    if line_arr[1] == ">":
                        self.min_air_humidity = float(line_arr[2])
                    else:
                        self.max_air_humidity = float(line_arr[2])

                # parsing soil humidity
                elif line_arr[0] == "soil_humidity":
                    if line_arr[1] == ">":
                        self.min_soil_humidity = float(line_arr[2])
                    else:
                        self.max_soil_humidity = float(line_arr[2])

                # parsing temp
                elif line_arr[0] == "air_temperature":
                    if line_arr[1] == ">":
                        self.min_air_temp = float(line_arr[2])
                    else:
                        self.max_air_temp = float(line_arr[2])

    def in_range_air_temp(self, temp):
        if temp < self.max_air_temp and temp > self.min_air_temp:
            return True
        return False

    def in_range_air_humid(self, humid):
        if humid < self.max_air_humidity and humid > self.min_air_humidity:
            return True
        return False

    def in_range_soil_humid(self, humid):
        if humid < self.max_soil_humidity and humid > self.min_soil_humidity:
            return True
        return False

    def print_range_values(self):
        print(f"max_air_humidity: {self.max_air_humidity}")
        print(f"min_air_humidity: {self.min_air_humidity} \n")

        print(f"max_soil_humidity: {self.max_soil_humidity}")
        print(f"min_soil_humidity: {self.min_soil_humidity}\n ")

        print(f"max_air_temp: {self.max_air_temp}")
        print(f"min_air_temp: {self.min_air_temp} \n")
