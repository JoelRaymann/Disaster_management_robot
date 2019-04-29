import io
import socket
import struct
import numpy as np
import sys
from PIL import Image
from cv2 import cv2 as cv

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
if len(sys.argv) != 3:
    print("{ERROR} Needs IP address and port as argument for starting server")

server_socket = socket.socket()
server_socket.bind((str(sys.argv[1]), int(sys.argv[2])))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    while True:
        # Exiting mechanism
        if cv.waitKey(1) & 0xFF == ord('q'):
            raise KeyboardInterrupt
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        image = Image.open(image_stream)
        imageData = np.array(image, dtype="float32")
        imageData /= 255.
        imageData = cv.cvtColor(imageData, cv.COLOR_BGR2RGB)
        cv.imshow("output", imageData)
        # print('Image is %dx%d' % image.size)
        # image.verify()
        # print('Image is verified')
        # img = cv.imread()

except Exception as err:
    print("{ERROR}: ", err)
    connection.close()
    server_socket.close()
    exit(1)

finally:
    connection.close()
    server_socket.close()