import datetime, os


def log_event(message):
    basedir = os.path.abspath(os.path.dirname(__file__))
    fd = open(f"{basedir}/../events_log.txt", "a")
    fd.write(
        f"{datetime.datetime.now().astimezone().strftime('%a %b %d %H:%M:%S %Z %Y')}: {message}\n"
    )
