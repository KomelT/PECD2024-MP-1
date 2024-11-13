from flask import Flask, request, jsonify
from rembg import remove, new_session
import numpy as np
import cv2


# Create a Flask app
app = Flask(__name__)

# Create a new rembg session
session = new_session("isnet-general-use")


@app.route("/process", methods=["GET"])
def process():

    try:
        # Load the image
        input_pic = request.files.get("image", "")

        if input_pic is None:
            return jsonify({"error": "No image file provided"}), 400

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

        # Return the yellow percentage as a JSON response
        return jsonify({"yellow_percentage": yellow_percentage})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0")
