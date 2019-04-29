import socket
import threading
from _thread import start_new_thread, exit_thread
from ExceptionHandler.ServerException import ServerException
from server_utilities.ServerUtilities import *
import sys
import RPi.GPIO as GPIO
import io
import struct
import time

def ControlListener(clientSocket:socket.socket, pin_set:tuple):
    '''
    Threaded function to listen to the client in a seperate
    thread and respond accordingly
    
    Arguments:
        clientSocket {socket.socket} -- the connected client socket

        pin_set {tuple} -- the set of input pins
    '''
    while True:
        try:
            command = clientSocket.recv(1024)
            command = command.decode("utf-8")
            # Run Commands
            if command == 'w':
                GoForward(pin_set)
            elif command == 's':
                GoBackward(pin_set)
            elif command == 'a':
                GoLeft(pin_set)
            elif command == 'd':
                GoRight(pin_set)
            elif command == 'q':
                Quit(pin_set)
                break
            elif command == 'o':
                Stop(pin_set)
            else:
                print("{ERROR} Wrong Command")
                
                
        except Exception as err:
            print("{Error} Uncaught exception: ", err)
            clientSocket.close()
            exit_thread(1)
    
    print("[INFO] Connection Closed")
    clientSocket.close()
    return True



def ControlServer(pin_set:tuple, host = "127.0.0.1", port = 5000):
    '''
    Function to start a server to control the bot at
    the specified host and port
    
    Arguments:
        pin_set {tuple} -- the set of input pins

    Keyword Arguments:
        host {str} -- the host ip address to host the server (default: {"127.0.0.1"})
        port {int} -- the host port address to host the server (default: {5000})
    '''

    # Starting server socket
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        raise ServerException(errorLevel = "Debug", errorMessage = "Server Socket Created")
    
    except socket.error as err:
        raise ServerException(errorLevel = "Critical", errorMessage = "Server Socket Not Created with error: {0}".format(err), log = True)
    
    except ServerException:
        True
    
    except Exception as err:
        print("{UnHandled ERROR}: ", err)
        raise ServerException(errorLevel = "Critical", errorMessage  = "Uncaught error: {0}".format(err), log = True)
        return False
    
    # Bind the socket
    serverSocket.bind((host, port))

    serverSocket.listen(5)
    print("[INFO] Socket is listening")

    while True:
        try:

            clientSocket, clientAddr = serverSocket.accept()
            print("[INFO] Got Connection from %s:%s" %(clientAddr[0], clientAddr[1]))

            start_new_thread(ControlListener, (clientSocket, pin_set, ))
        
        except KeyboardInterrupt:
            print("[+] Ending Processes")
            serverSocket.close()
            break

        except Exception as err:
            print("{Error} Uncaught exception: ", err)
            serverSocket.close()
            exit(1)
    return True



if __name__ == "__main__":
        
    localhost = "127.0.0.1"
    port = 5000
    if len(sys.argv) == 3:
        localhost = sys.argv[1]
        port = int(sys.argv[2])

    # Setup GPIO Connections
    GPIO.setmode(GPIO.BOARD)

    try:
        # input Pins
        leftPinForward = 3
        leftPinBackward = 5
        leftMotorEnable = 8
        rightPinForward = 11
        rightPinBackward = 13
        rightMotorEnable = 10

        pin_set = (leftMotorEnable, rightMotorEnable, leftPinForward, leftPinBackward, rightPinForward, rightPinBackward)


        # Setup Pins
        GPIO.setup(leftMotorEnable, GPIO.OUT, initial = 0)
        GPIO.setup(leftPinForward, GPIO.OUT, initial = 0)
        GPIO.setup(leftPinBackward, GPIO.OUT, initial = 0)
        GPIO.setup(rightMotorEnable, GPIO.OUT, initial = 0)
        GPIO.setup(rightPinForward, GPIO.OUT, initial = 0)
        GPIO.setup(rightPinBackward, GPIO.OUT, initial = 0)

        # Enable Pins
        GPIO.output(leftMotorEnable, GPIO.HIGH)
        GPIO.output(rightMotorEnable, GPIO.HIGH)

        # NOTE:RESET
        GPIO.output(leftPinForward, GPIO.LOW)
        GPIO.output(leftPinBackward, GPIO.LOW)
        GPIO.output(rightPinForward, GPIO.LOW)
        GPIO.output(rightPinBackward, GPIO.LOW)

        
        start_new_thread(ControlServer, (pin_set, localhost, port, ))
    except Exception as err:
        print("{ERROR}:", err)
    
    finally:
        GPIO.cleanup()
