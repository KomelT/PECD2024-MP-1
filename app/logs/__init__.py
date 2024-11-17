from datetime import datetime
from os import path


def log_event(message):
    basedir = path.abspath(path.dirname(__file__))
    fd = open(f"{basedir}/../events_log.txt", "a")
    fd.write(
        f"{datetime.now().astimezone().strftime('%a %b %d %H:%M:%S %Z %Y')}: {message}\n"
    )
    fd.close()


def is_daylight():
    # Get the current time
    current_time = datetime.now().time()

    # Define the start and end times
    start_time = datetime.strptime("06:00:00", "%H:%M:%S").time()
    end_time = datetime.strptime("19:00:00", "%H:%M:%S").time()

    # Check if the current time is between 6:00 AM and 7:00 PM
    return start_time <= current_time <= end_time
