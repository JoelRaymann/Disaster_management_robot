import socket
from pynput.keyboard import Key, KeyCode, Listener
from _thread import exit_thread

clientSocket = None

def GoForward(clientSocket:socket.socket):
    '''
    Function to go forward --> on press: w
    
    Arguments:
        clientSocket {socket.socket} -- The client side socket used to send data to RPi bot
    '''
    clientSocket.send("w".encode("utf-8"))
    print("[+] Going Forward")

def GoBackward(clientSocket:socket.socket):
    '''
    Function to go backward --> on press: s
        
    Arguments:
        clientSocket {socket.socket} -- The client side socket used to send data to RPi bot
    '''
    clientSocket.send("s".encode("utf-8"))
    print("[+] Going Backward")



def GoLeft(clientSocket: socket.socket):
    '''
    Function to turn left --> on press: a
        
    Arguments:
        clientSocket {socket.socket} -- The client side socket used to send data to RPi bot
    '''
    clientSocket.send("a".encode("utf-8"))
    print("[+] Going left")

def GoRight(clientSocket: socket.socket):
    '''
    Function to go right --> on press: d
        
    Arguments:
        clientSocket {socket.socket} -- The client side socket used to send data to RPi bot
    '''
    print("[+] Turning Right")
    clientSocket.send("d".encode("utf-8"))

def Stop(clientSocket:socket.socket):
    '''
    Function to stop the bot --> on release: all keys
        
    Arguments:
        clientSocket {socket.socket} -- The client side socket used to send data to RPi bot
    '''
    clientSocket.send("o".encode("utf-8"))
    print("[+] Bot Stopped")

def Quit(clientSocket: socket.socket):
    '''
    Function to quit the controls
        
    Arguments:
        clientSocket {socket.socket} -- The client side socket used to send data to RPi bot
    '''
    clientSocket.send("q".encode("utf-8"))
    print("[+] Quitting")

def _on_press(key):
    '''
    Function to handle the on press 
    NOTE: PRIVATE FUNCTION
    Arguments:
        key {KeyCode} -- The response Hooked key
    '''
    if key == KeyCode(char = "w"):
        GoForward(clientSocket)
    elif key == KeyCode(char = "a"):
        GoLeft(clientSocket)
    elif key == KeyCode(char = "s"):
        GoBackward(clientSocket)
    elif key == KeyCode(char = "d"):
        GoRight(clientSocket)
    elif key == KeyCode(char = "q"):
        print("[+] Quiting")
        Quit(clientSocket)
        exit_thread()
        return False
    else:
        print("{ERROR}: Wrong command]")

def _on_release(key):
    '''
    Function to handle the on release
    NOTE: PRIVATE FUNCTION
    Arguments:
        key {KeyCode} -- The response Hooked Key
    '''
    if key in [KeyCode(char = "w"), KeyCode(char = "a"), KeyCode(char = "s"), KeyCode(char = "d")]:
        Stop(clientSocket)
    elif key == KeyCode(char = "q"):
        exit_thread()
        return False
    else:
        pass



def ControlBot(*args, **kwargs):
    '''
    Function to control the bot using threading. Define the clientSocket in the module before use
    '''
    while(True):
        try:
            with Listener(on_press = _on_press, on_release = _on_release) as listener:
                listener.join()
            break
            
        except KeyboardInterrupt:
            print("[+] Exiting")
            clientSocket.close()
            break
        
        except Exception as err:
            print("{ERROR} :", err)
            clientSocket.close()
            break
            
## For Testing
# if __name__ == "__main__":
#     print("[INFO] Starting Bot")
#     ControlBot()

