class Camera:
    def __init__(self, sever_address="http://localhost:5000", local_mode=False):
        print("[INFO] Camera init")
        
        self.sever_address = sever_address
        self.local_mode = local_mode

        if self.local_mode:
            from os import path, environ
            from rembg import new_session
            
            basedir = path.abspath(path.dirname(__file__))
            environ["U2NET_HOME"] = f"{basedir}/u2net"

            # Create a new rembg session
            self.session = new_session("isnet-general-use")

    def get_percentage(self):
        from picamera2 import Picamera2
        from io import BytesIO
        
        print("[INFO] Getting image")

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
        
        from requests import get

        r = get(self.sever_address, files={"image": pic.getvalue()})
        return r.json()

    def process(self, input_pic):
        from numpy import frombuffer, array, uint8
        from cv2 import imdecode, IMREAD_COLOR, cvtColor, COLOR_BGR2HSV, inRange, countNonZero
        from rembg import remove
        
        print("[INFO] Processing image")

        # Remove the background using rembg
        output = remove(input_pic, session=self.session, force_return_bytes=True)

        # Decode the processed image into an OpenCV format
        pic_bg = imdecode(frombuffer(output, uint8), IMREAD_COLOR)

        # Convert the image to HSV color space
        hsv_image = cvtColor(pic_bg, COLOR_BGR2HSV)

        # Define HSV range for yellow color
        lower_yellow = array([20, 100, 100])
        upper_yellow = array([30, 255, 255])

        # Create a mask to capture areas in the yellow range
        yellow_mask = inRange(hsv_image, lower_yellow, upper_yellow)

        # Calculate the percentage of yellow pixels in the image
        yellow_percentage = (countNonZero(yellow_mask) / yellow_mask.size) * 100

        # For black color
        lower_black = array([0, 0, 0])
        upper_black = array([180, 255, 50])
        black_mask = inRange(hsv_image, lower_black, upper_black)
        black_percentage = (countNonZero(black_mask) / black_mask.size) * 100

        # For green color
        lower_green = array([35, 100, 100])
        upper_green = array([85, 255, 255])
        green_mask = inRange(hsv_image, lower_green, upper_green)
        green_percentage = (countNonZero(green_mask) / green_mask.size) * 100

        # Return the yellow, green and black percentage as a JSON response
        return {
            "yellow_percentage": yellow_percentage,
            "green_percentage": green_percentage,
            "black_percentage": black_percentage,
        }
