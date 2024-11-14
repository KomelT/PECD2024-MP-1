from picamera2 import Picamera2
import time, json
from io import BytesIO
import requests

class Camera:
    def __init__(self, sever_address="http://localhost:5000"):
        self.sever_address = sever_address

    def get_percentage(self):
        # Init the camera
        picam2 = Picamera2()
        config = picam2.create_still_configuration(
            {"format": "RGB888", "size": (4056, 3040)}
        )
        picam2.configure(config)
        picam2.start()

        time.sleep(2)

        pic = BytesIO()
        picam2.capture_file(pic, format="jpeg")
        picam2.stop()

        r = requests.get(self.sever_address, files={"image": pic.getvalue()})
       # percentage = json.loads(str(r))
        return r.json()
    
