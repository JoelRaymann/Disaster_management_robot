import socket
import threading
from _thread import start_new_thread, exit_thread
import sys
import io
import struct
import time
import picamera

def ControlVideoClient(host = "127.0.0.1", port = 8000):
    '''
    Function to start a client connection to run video stream
    
    Keyword Arguments:
        host {str} -- The ip address to connect to the port (default: {"127.0.0.1"})
        port {int} -- The port to connect to the video server (default: {8000})
    '''
    client_socket = socket.socket()
    print("[INFO] Client Socket for Video Streaming initiated")
    print("[INFO] Connecting to %s: %d" %(host, port))
    client_socket.connect((host, 8000))
    connection = client_socket.makefile('wb')
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.framerate = 30
            time.sleep(2)
            start = time.time()
            count = 0
            stream = io.BytesIO()
            # Use the video-port for captures...
            for _ in camera.capture_continuous(stream, 'jpeg',use_video_port=True):
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
                stream.seek(0)
                connection.write(stream.read())
                count += 1
                # if time.time() - start > 30:
                #     break
                stream.seek(0)
                stream.truncate()
    
    except socket.error:
        print("{Connection} Closed")
        
    except Exception as err:
        print("{ERROR} :", err)

    finally:
        connection.write(struct.pack('<L', 0))
        connection.close()
        client_socket.close()
        finish = time.time()
    print('Sent %d images in %d seconds at %.2ffps' % (count, finish-start, count / (finish-start)))
    return True
    
if __name__ == "__main__":
        
    localhost = "127.0.0.1"
    port = 8000
    if len(sys.argv) == 3:
        localhost = sys.argv[1]
        port = int(sys.argv[2])
    try:
        start_new_thread(ControlVideoClient, (localhost, port, ))

    except Exception as err:
        print("{ERROR}:", err)