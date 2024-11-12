
import cv2
from PIL import Image
import time
import numpy as np
from time import sleep
import matplotlib.pyplot as plt
from io import BytesIO

from picamera2 import Picamera2 


import socket
import numpy as np
#from io import BytesIO
#import cv2

'''
THIS IS THE CODE FOR THE CLIENT-SIDE of the background removal API
'''
PORT = 8000


def get_size(buf):
    header = buf[:4].decode()
    if header=='SIZE':
        size = int.from_bytes(buf[5:9],byteorder='little') 
        return size
    raise RuntimeError("Decodification of the size parameter from the header failed. (Wrong header?)")

# pic must be bytes
def get_leaf_color_means(pic, dir_serv,size):
    s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    s.connect((dir_serv,PORT) )

    if not pic:
        raise ValueError("Image is empty")
    size_b =  int.to_bytes(size,4,byteorder='little')  
    
    s.sendall(b'SIZE ' + size_b + b' '+ pic)
    print(f"Image sended ( {size} bytes )")

    cont = 0
    # first block and size
    buf = s.recv(256)
    cont += len(buf)
    size = get_size(buf)
        
    calculated_means = buf[10:]
    while cont < size:
        buf = s.recv(4096)
        calculated_means += buf
        cont += len(buf)
    mean_arr = np.frombuffer(calculated_means, dtype=float) # cv2.IMREAD_COLOR in OpenCV 3.1
    s.close()
    return (mean_arr)
 


def get_percentage():
    picam2 = Picamera2()
    config = picam2.create_still_configuration({'format': 'RGB888', 'size': (4056, 3040)})
    picam2.configure(config)

    picam2.start()

    time.sleep(2)
    data = BytesIO()
    picam2.capture_file(data, format='jpeg')
    picam2.stop()
    data_b = data.getvalue()
    size = len(data_b)
    mean_arr = get_leaf_color_means(data_b,"ordenador",size)
    print(f"Green mean: {mean_arr[0]} \n Yellow mean: {mean_arr[1]} \n Black mean: {mean_arr[2]}")

