import numpy as np
import socket, os, signal
from rembg import remove, new_session
import cv2
import matplotlib.pyplot as plt

'''
THIS IS THE CODE FOR THE SERVER-SIDE of the background removal API
'''
    
def plot_histograms(green_intensity, yellow_intensity, black_intensity):
    # Plot and save histogram for yellow intensities with specific scaling
    plt.figure(figsize=(8, 6))
    plt.hist(yellow_intensity, bins=30, color='yellow', edgecolor='black')
    plt.title("Histogram of Yellow Intensities in the Image")
    plt.xlabel("Intensity")
    plt.ylabel("Frequency")
    yellow_output_path = 'yellow_histogram.png'
    plt.savefig('yellow_histogram.png')
    plt.close()  # Close the plot after saving

    # Plot and save histogram for green intensities with specific scaling
    plt.figure(figsize=(8, 6))
    plt.hist(green_intensity, bins=30, color='green', edgecolor='black')
    plt.title("Histogram of Green Intensities in the Image")
    plt.xlabel("Intensity")
    plt.ylabel("Frequency")
    green_output_path = 'green_histogram.png'
    plt.savefig(green_output_path)    
    plt.close()  # Close the plot after saving
    
        # Plot and save histogram for green intensities with specific scaling
    plt.figure(figsize=(8, 6))
    plt.hist(black_intensity, bins=30, color='black', edgecolor='red')
    plt.title("Histogram of Green Intensities in the Image")
    plt.xlabel("Intensity")
    plt.ylabel("Frequency")
    black_output_path = 'black_histogram.png'
    plt.savefig(black_output_path)    
    plt.close()  # Close the plot after saving
    
    print(f"Yellow histogram saved to: {yellow_output_path}")
    print(f"Green histogram saved to: {green_output_path}")
    print(f"Black histogram saved to: {black_output_path}")

# Calculate intensity of the colors
# set plot_histogram True for plotting the histrogram
def get_color_intensity(image_rgb, plot_histogram):
    # Define yellow mask: red and green channels should be high, blue should be low
    yellow_mask = (image_rgb[:, :, 0] > 150) & (image_rgb[:, :, 1] > 150) & (image_rgb[:, :, 2] < 100)
    yellow_pixels = image_rgb[yellow_mask]
    yellow_intensity = (yellow_pixels[:, 0] + yellow_pixels[:, 1]) / 2

    # Define green mask: green channel should be high, red and blue channels low
    green_mask = (image_rgb[:, :, 1] > 150) & (image_rgb[:, :, 0] < 100) & (image_rgb[:, :, 2] < 100)
    green_pixels = image_rgb[green_mask]
    green_intensity = green_pixels[:, 1]  
    
    # Threshold for detecting black pixels (low R, G, and B channels)
    black_threshold = 50 
    mask_black = (image_rgb[:, :, 0] < black_threshold) &  (image_rgb[:, :, 1] < black_threshold) & (image_rgb[:, :, 2] < black_threshold)
    black_pixels = image_rgb[mask_black]
    black_intensity = (black_pixels[:, 0] + black_pixels[:, 1]+ black_pixels[:, 2]) / 3

    if (plot_histogram):
       plot_histograms(green_intensity, yellow_intensity, black_intensity)   
       
    return green_intensity, yellow_intensity, black_intensity


def get_mean_intensity(green_intensity, yellow_intensity, black_intensity):
    # Calculate mean intensity
    green_m = round(np.mean(green_intensity),2)
    yellow_m = round(np.mean(yellow_intensity),2)
    #median_yellow_intensity = np.median(yellow_intensity)
    black_m = round(np.mean(black_intensity),2)



    arr = np.array([green_m, yellow_m, black_m])
    return (arr)
    
def get_size(buf):
    header = buf[:4].decode()
    if header=='SIZE':
        size = int.from_bytes(buf[5:9],byteorder='little') 
        return size
    raise RuntimeError

PORT = 8000
basedir = os.path.abspath(os.path.dirname(__file__))
os.environ['U2NET_HOME'] = basedir + '/u2net' # path to trained model

model_name = "isnet-general-use"
session = new_session(model_name)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dt = np.uint8  # datatype

s.bind(('', PORT))
s.listen(5)

while True:
    dialog, dir_cli = s.accept()
    print(f"Client connected from {dir_cli[0]}:{dir_cli[1]}.")

    try:
        cont = 0
        # first block and size
        buf = dialog.recv(256)
        cont += len(buf)
        size = get_size(buf)
        input_pic = buf[10:]
        
        print(f"Size of the upcoming image is {size} B")
        while cont < size:
            # receive pic from the client
            buf = dialog.recv(1024)
            input_pic += buf
            cont += len(buf)

        print("I got the image")
    
        output = remove(input_pic, session=session, force_return_bytes=True)
        output1 = cv2.imdecode(np.frombuffer(output, dt),cv2.IMREAD_COLOR) # cv2.IMREAD_COLOR in OpenCV 3.1


        # Convert the image to HSV color space
        hsv_image = cv2.cvtColor(output1, cv2.COLOR_BGR2HSV)

        # Define HSV range for yellow color (you might need to adjust these values)
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])

        # Create a mask that captures areas in the yellow range
        yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

        # Calculate the percentage of yellow pixels in the image
        yellow_percentage = (cv2.countNonZero(yellow_mask) / yellow_mask.size) * 100

        print(f"Yellow area percentage: {yellow_percentage:.2f}%")

        # Decide if the plant is turning yellow based on a threshold
        if yellow_percentage > 5:  # Adjust threshold as needed
            print("The plant is showing signs of yellowing.")
        else:
            print("The plant appears healthy.")



        cv2.imwrite('img_without_bg.jpg',output1) # cv2 uses BGR by default
        
        image_rgb = cv2.cvtColor(output1, cv2.COLOR_BGR2RGB)
        
        green_intensity, yellow_intensity, black_intensity = get_color_intensity(image_rgb, True)
        mean_arr = get_mean_intensity(green_intensity, yellow_intensity, black_intensity)
        print(f"Green mean: {mean_arr[0]} \n Yellow mean: {mean_arr[1]} \n Black mean: {mean_arr[2]}")
        mean_arr_b = mean_arr.tobytes()        
        dialog.sendall(b'SIZE ' + int.to_bytes(len(mean_arr_b) ,4,byteorder='little') + b' '+ mean_arr_b) 
        print("Image processed. End of session received...")
        dialog.close()

    except Exception as e:
        print(f"Error during processing: {e}")
        dialog.close()  # Close the client connection
        break
s.close()



