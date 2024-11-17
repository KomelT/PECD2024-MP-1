from os import path, system, remove
from json import load, JSONDecodeError, dump
from signal import signal, SIGINT, SIGTERM
from RPi import GPIO

basedir = path.abspath(path.dirname(__file__))


class State:
    def __init__(self, file_location=f"{basedir}/../leaf_state.json"):
        print("[INFO] State init")
        self.file_location = file_location
        self.plant_yellow_percentage = 0
        self.plant_black_percentage = 0
        self.halted = False
        self.waking_up = False
        self.get_state_from_file()
        signal(SIGINT, self.ctrl_c_handler)
        signal(SIGTERM, self.ctrl_c_handler)
        self.dump_state()

    def get_state_from_file(self):
        try:
            with open(self.file_location, "r") as file:
                data = load(file)
                self.plant_yellow_percentage = data["plant_yellow_percentage"]
                self.plant_black_percentage = data["plant_black_percentage"]
                self.halted = data["halted"]
        except FileNotFoundError:
            self.waking_up = True
            print("[INFO] State file does not exist.")
        except JSONDecodeError:
            self.waking_up = True
            print("[INFO] State file is not valid ")

    def dump_state(self):
        data = {
            "plant_yellow_percentage": self.plant_yellow_percentage,
            "plant_black_percentage": self.plant_black_percentage,
            "halted": self.halted,
        }
        with open(self.file_location, "w") as file:
            dump(data, file)
            file.close()

    def set_plant_yellow_black_percentage(self, yellow_percentage, black_percentage):
        self.plant_yellow_percentage = yellow_percentage
        self.plant_black_percentage = black_percentage
        self.dump_state()

    def halt(self):
        GPIO.cleanup()
        self.halted = True
        self.dump_state()
        system("sudo poweroff")
        exit(0)

    def ctrl_c_handler(self, signum, frame):
        GPIO.cleanup()
        remove(self.file_location)
        print("[INFO] Exiting...")
        exit(0)
