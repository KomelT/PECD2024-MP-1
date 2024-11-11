import socket
import numpy as np
from io import BytesIO

PORT = 8000


def get_size(buf):
    header = buf[:4].decode()
    if header=='SIZE':
        size = int.from_bytes(buf[5:9],byteorder='little') 
        return size
    print('something was wrong while decoding the size from the header')
    raise RuntimeError

# pic must be bytes
def remove_bg_send(pic, dir_serv,size):
    s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    s.connect((dir_serv,PORT) )
    dt = np.uint8

    while True:
        if not pic:
            print("Image is empty")
            break
        size_b =  int.to_bytes(size,4,byteorder='little')  
        
        s.sendall(b'SIZE ' + size_b + b' '+ pic)
        print(f"Image sended ( {size} bytes )")

        cont = 0
        # first block and size
        buf = s.recv(256)
        cont += len(buf)
        size = get_size(buf)
           
        processed_pic = buf[10:]
        while cont < size:
            buf = s.recv(4096)
            processed_pic += buf
            cont += len(buf)
        return (processed_pic)
    s.close()
 
    
if __name__ == "__main__":
    with open("../foto.jpg", "rb") as fd:
        pic = BytesIO(fd.read()).getvalue()
    
    size = len(pic)
    output_bytes = remove_bg_send(pic,"127.0.0.1",size)
    
    with open("output_main.png", "wb") as f:
        f.write(output_bytes)
    