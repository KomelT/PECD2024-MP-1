
import cv2
from PIL import Image
import time
import numpy as np
from time import sleep
import matplotlib.pyplot as plt
from rem_bg import remove_bg_send
from io import BytesIO

from picamera2 import Picamera2 

picam2 = Picamera2()
#capture_config = picam2.create_still_configuration()
#picam2.configure(picam2.create_preview_configuration())
config = picam2.create_still_configuration({'format': 'RGB888', 'size': (4056, 3040)})
picam2.configure(config)

picam2.start()

time.sleep(2)
data = BytesIO()
picam2.capture_file(data, format='jpeg')
picam2.stop()
data_b = data.getvalue()

pic = remove_bg_send(data_b,"ordenador",len(data_b))
pic_buf = BytesIO(pic)
dt = np.uint8

'''
with open("../leaf_yellow.jpg", "rb") as fd:
    pic = BytesIO(fd.read()).getvalue()
    
img_bytes = remove_bg_send(pic,"127.0.0.1",len(pic))
'''


pic = cv2.imdecode(np.frombuffer(pic, dt),cv2.IMREAD_COLOR) # cv2.IMREAD_COLOR in OpenCV 3.1
cv2.imwrite('img.jpg',pic) # cv2 uses BGR by default 

image_rgb = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)

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

porcentaje_negro = np.sum(mask_negra) / mask_negra.size * 100

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


# Percentage of yellow pixels
percentage_yellow = np.sum(yellow_mask) / yellow_mask.size * 100
print(f'Percentage of yellow: {percentage_yellow:.2f}%')

# Percentage of green pixels
percentage_green = np.sum(green_mask) / green_mask.size * 100
print(f'Percentage of green: {percentage_green:.2f}%')




# Define a threshold for detecting black pixels (low values in R, G, and B channels)
black_threshold = 50  # Pixels with R, G, and B values below this threshold are considered black

# Create a mask where Red, Green, and Blue channels are below the threshold (detecting black areas)
mask_black = (image_rgb[:, :, 0] < black_threshold) &  (image_rgb[:, :, 1] < black_threshold) & (image_rgb[:, :, 2] < black_threshold)

# Calculate the percentage of black pixels
percentage_black = np.sum(black_mask) / black_mask.size * 100
print(f'Percentage of black pixels: {percentage_black:.2f}%')