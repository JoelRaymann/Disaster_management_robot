from pynput.keyboard import Key, Listener, KeyCode
from server_utilities.ServerUtilitiesTest import *

w = KeyCode(char = "w")
q = KeyCode(char = "q")
pinset = (1, 2, 3, 4, 5, 6)

def on_press(key):
    if key == w:
        GoForward(pinset)

def on_release(key):
    Stop(pinset)
    if key == q:
        Quit(pinset)
        return False

with Listener(on_press = on_press, on_release = on_release) as listener:
    listener.join()