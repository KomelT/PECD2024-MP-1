from picamera2 import Picamera2
from io import BytesIO
import requests
from rembg import remove, new_session
import numpy as np
import cv2


class Camera:
    def __init__(self, sever_address="http://localhost:5000", local_mode=False):
        self.sever_address = sever_address
        self.local_mode = local_mode

    def get_percentage(self):
        # Init the camera
        picam2 = Picamera2()
        config = picam2.create_still_configuration(
            {"format": "RGB888", "size": (1920, 1080)}
        )
        picam2.configure(config)
        picam2.start()

        pic = BytesIO()
        picam2.capture_file(pic, format="jpeg")
        picam2.stop()

        if self.local_mode:
            return self.process(pic.getvalue())

        r = requests.get(self.sever_address, files={"image": pic.getvalue()})
        return r.json()

    def process(self, input_pic):
        # Create a new rembg session
        session = new_session("isnet-general-use")

        # Read the image data as bytes
        input_bytes = input_pic.read()

        # Remove the background using rembg
        output = remove(input_bytes, session=session, force_return_bytes=True)

        # Decode the processed image into an OpenCV format
        pic_bg = cv2.imdecode(np.frombuffer(output, np.uint8), cv2.IMREAD_COLOR)

        # Convert the image to HSV color space
        hsv_image = cv2.cvtColor(pic_bg, cv2.COLOR_BGR2HSV)

        # Define HSV range for yellow color
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])

        # Create a mask to capture areas in the yellow range
        yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

        # Calculate the percentage of yellow pixels in the image
        yellow_percentage = (cv2.countNonZero(yellow_mask) / yellow_mask.size) * 100

        # For black color
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 255, 50])
        black_mask = cv2.inRange(hsv_image, lower_black, upper_black)
        black_percentage = (cv2.countNonZero(black_mask) / black_mask.size) * 100

        # For green color
        lower_green = np.array([35, 100, 100])
        upper_green = np.array([85, 255, 255])
        green_mask = cv2.inRange(hsv_image, lower_green, upper_green)
        green_percentage = (cv2.countNonZero(green_mask) / green_mask.size) * 100

        # Return the yellow, green and black percentage as a JSON response
        return {
            "yellow_percentage": yellow_percentage,
            "green_percentage": green_percentage,
            "black_percentage": black_percentage,
        }
