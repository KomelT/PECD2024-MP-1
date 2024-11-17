import datetime
import os


def log_event(message):
    basedir = os.path.abspath(os.path.dirname(__file__))
    fd = open(f"{basedir}/../events_log.txt", "a")
    fd.write(
        f"{datetime.datetime.now().astimezone().strftime('%a %b %d %H:%M:%S %Z %Y')}: {message}\n"
    )
    fd.close()


def is_daylight():
    # Get the current time
    current_time = datetime.datetime.now().time()

    # Define the start and end times
    start_time = datetime.datetime.strptime("06:00:00", "%H:%M:%S").time()
    end_time = datetime.datetime.strptime("19:00:00", "%H:%M:%S").time()

    # Check if the current time is between 6:00 AM and 7:00 PM
    return start_time <= current_time <= end_time
