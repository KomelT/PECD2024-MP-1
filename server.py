import numpy as np
import socket, os, signal
from rembg import remove, new_session


def get_size(buf):
    header = buf[:4].decode()
    if header=='SIZE':
        size = int.from_bytes(buf[5:9],byteorder='little') 
        return size
    raise RuntimeError

PORT = 40007
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
    
        output = remove(input_pic, session=session, force_return_bytes=True) #### 1D ARRAY CONVERTIDO A BYTES ES lo mismo que lo que devuelva esta funcion en bytes?

        output_size = int.to_bytes(len(output),4,byteorder='little')  
        dialog.sendall(b'SIZE ' + output_size + b' '+  output) 
        print("Image processed. End of session received...")
        dialog.close()

    except Exception as e:
        print(f"Error during processing: {e}")
        dialog.close()  # Close the client connection
        break
s.close()



