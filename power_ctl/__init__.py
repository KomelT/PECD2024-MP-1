import json, os
from parser import *

JSON_FILE = "leaf_state.json"

# must be a dict variable (get_percentage output)
def save_leaf_current_state(color_percentage):
    with open(JSON_FILE, 'w', encoding='utf-8') as file:
        json.dump(color_percentage, file, ensure_ascii=False, indent=4)
    print(f"JSON file saved as {JSON_FILE}")
    
    
# It returns true if it was halted before
def was_it_halted():
    return os.path.exists(JSON_FILE)
 
 # must be a dict variable (get_percentage output)
def read_leaf_current_state():
    try:
        with open(JSON_FILE, 'r') as file:
            leaf_state = json.load(file)
    except FileNotFoundError:
        print("The file does not exist.")
    except json.JSONDecodeError:
        print("The file is not valid JSON.")
    return leaf_state


def retrieve_prev_state(parser):
        leaf = read_leaf_current_state()
        parser.set_colors_baseline_mean(leaf['green_percetange'],leaf['yellow_percetange'],leaf['black_percetange'])
        print("Previous state retrieved")
    
    
         