import os
import json
import signal


basedir = os.path.abspath(os.path.dirname(__file__))


class State:
    def __init__(self, file_location=f"{basedir}/../leaf_state.json"):
        print("[INFO] State init")
        self.file_location = file_location
        self.plant_yellow_percentage = 0
        self.plant_black_percentage = 0
        self.halted = False
        self.waking_up = False
        self.get_state_from_file()
        signal.signal(signal.SIGINT, self.ctrl_c_handler)
        signal.signal(signal.SIGTERM, self.ctrl_c_handler)

    def get_state_from_file(self):
        try:
            with open(self.file_location, "r") as file:
                data = json.load(file)
                self.plant_yellow_percentage = data["plant_yellow_percentage"]
                self.plant_black_percentage = data["plant_black_percentage"]
                self.halted = data["halted"]
        except FileNotFoundError:
            self.waking_up = True
            print("State file does not exist.")
        except json.JSONDecodeError:
            self.waking_up = True
            print("State file is not valid JSON.")

    def dump_state(self):
        data = {
            "plant_yellow_percentage": self.plant_yellow_percentage,
            "plant_black_percentage": self.plant_black_percentage,
            "halted": self.halted,
        }
        with open(self.file_location, "w") as file:
            json.dump(data, file)

    def set_plant_yellow_black_percentage(self, yellow_percentage, black_percentage):
        self.plant_yellow_percentage = yellow_percentage
        self.plant_black_percentage = black_percentage
        self.dump_state()

    def halt(self):
        self.halted = True
        self.dump_state()
        os.system("sudo poweroff")
        exit(0)

    def ctrl_c_handler(self, signum, frame):
        os.remove(self.file_location)
        print("Exiting...")
        exit(0)
