
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
