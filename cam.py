
import cv2
from PIL import Image

import numpy as np
from time import sleep
import matplotlib.pyplot as plt
from client import remove_bg_send
from io import BytesIO
'''
from picamera2 import Picamera2 

#resolution = (4056, 3040)
#config = picam2.create_still_configuration(raw={'format': 'SBGGR12', 'size': (4056, 3040)})


picam2 = Picamera2()
capture_config = picam2.create_still_configuration()
picam2.configure(picam2.create_preview_configuration())
picam2.start()

time.sleep(1)
data = io.BytesIO()
picam2.capture_file(data, format='jpeg')


pic = remove_bg_send(data.getvalue(),"127.0.0.1")
#pic = pic.reshape((240, 320, 3))
pic_buf = io.BytesIO(pic)
_ = raw_image_buffer.seek(0)
image = Image.open(pic_buf)


'''
with open("../leaf_yellow.jpg", "rb") as fd:
    pic = BytesIO(fd.read()).getvalue()

dt = np.uint8
img_bytes = remove_bg_send(pic,"127.0.0.1",len(pic))
image = cv2.imdecode(np.frombuffer(img_bytes, dt),cv2.IMREAD_COLOR) # cv2.IMREAD_COLOR in OpenCV 3.1


#image_rgb = cv2.imread("../yellow.jpg", cv2.IMREAD_COLOR)

cv2.imwrite('img.jpg',image) # cv2 ses BGR by default ( ithink)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Define yellow mask: red and green channels should be high, blue should be low
yellow_mask = (image_rgb[:, :, 0] > 150) & (image_rgb[:, :, 1] > 150) & (image_rgb[:, :, 2] < 100)
yellow_pixels = image_rgb[yellow_mask]
yellow_intensity = (yellow_pixels[:, 0] + yellow_pixels[:, 1]) / 2
print(yellow_intensity)
print(f"Yellow array reduction: {sum(yellow_intensity)}")

# Define green mask: green channel should be high, red and blue channels low
green_mask = (image_rgb[:, :, 1] > 150) & (image_rgb[:, :, 0] < 100) & (image_rgb[:, :, 2] < 100)
green_pixels = image_rgb[green_mask]
green_intensity = green_pixels[:, 1]  # Use the green channel for green intensity
print(green_intensity)
print(f"Green array reduction: {sum(green_intensity)}")



# Plot and save histogram for yellow intensities with specific scaling
plt.figure(figsize=(8, 6))
plt.hist(yellow_intensity, bins=30, color='yellow', edgecolor='black')
plt.title("Histogram of Yellow Intensities in the Image")
plt.xlabel("Intensity")
plt.ylabel("Frequency")
yellow_output_path = 'yellow_histogram.png'  # Define your desired output path and file name
plt.savefig(yellow_output_path)
plt.close()  # Close the plot after saving

# Plot and save histogram for green intensities with specific scaling
plt.figure(figsize=(8, 6))
plt.hist(green_intensity, bins=30, color='green', edgecolor='black')
plt.title("Histogram of Green Intensities in the Image")
plt.xlabel("Intensity")
plt.ylabel("Frequency")
green_output_path = 'green_histogram.png'  # Define your desired output path and file name
plt.savefig(green_output_path)
plt.close()  # Close the plot after saving

print(f"Yellow histogram saved to: {yellow_output_path}")
print(f"Green histogram saved to: {green_output_path}")