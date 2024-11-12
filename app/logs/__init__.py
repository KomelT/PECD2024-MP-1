import datetime


def log_event(message):
    fd = open("./events_log.txt", "a")
    fd.write(
        f"{datetime.datetime.now().astimezone().strftime('%a %b %d %H:%M:%S %Z %Y')}: {message}\n"
    )
