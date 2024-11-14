import json, os
from parser import *


class State:
    def __init__(self, file_location="./leaf_state.json"):
        self.file_location = file_location
        self.plant_yellow_percentage = 0
        self.halted = False

        get_state_from_file()


def get_state_from_file(self):
    try:
        with open(self.file_location, "r") as file:
            data = json.load(file)
            self.plant_yellow_percentage = data["plant_yellow_percentage"]
            self.halted = data["halted"]
    except FileNotFoundError:
        print("The file does not exist.")
    except json.JSONDecodeError:
        print("The file is not valid JSON.")


def dump_state(self):
    data = {
        "plant_yellow_percentage": self.plant_yellow_percentage,
        "halted": self.halted,
    }
    with open(self.file_location, "w") as file:
        json.dump(data, file)


def set_plant_yellow_percentage(self, percentage):
    self.plant_yellow_percentage = percentage
    dump_state()


def halt(self):
    self.halted = True
    dump_state()
    os.system("poweroff")
    exit(0)
