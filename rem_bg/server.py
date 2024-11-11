import numpy as np
import socket, os, signal
from rembg import remove, new_session
    
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
    plt.savefig('green_histogram.png')    
    plt.close()  # Close the plot after saving
    
    print(f"Yellow histogram saved to: {yellow_output_path}")
    print(f"Green histogram saved to: {green_output_path}")

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


def get_color_percentage(green_intensity, yellow_intensity, black_intensity):
    # Calculate the percentage of black pixels
    percentage_black = np.sum(mask_black) / mask_black.size * 100
    print(f'Percentage of black pixels: {percentage_black:.2f}%')

    return green_intensity, yellow_intensity, black_intensity
    
def get_size(buf):
    header = buf[:4].decode()
    if header=='SIZE':
        size = int.from_bytes(buf[5:9],byteorder='little') 
        return size
    raise RuntimeError

PORT = 4444
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
    
        output = remove(input_pic, session=session)
        cv2.imwrite('img_without_bg.jpg',output) # cv2 uses BGR by default 
        image_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        
        green_intensity, yellow_intensity, black_intensity = get_color_intensity(image_rgb, True)
        green_percentage, yellow_percentage, black_percentage = get_color_percentage(green_intensity, yellow_intensity, black_intensity)
        
        
        
        
        
        


       # output_size = int.to_bytes(len(output),4,byteorder='little')  
       # dialog.sendall(b'SIZE ' + output_size + b' '+  output) 
        
        
        
        
        print("Image processed. End of session received...")
        dialog.close()

    except Exception as e:
        print(f"Error during processing: {e}")
        dialog.close()  # Close the client connection
        break
s.close()



