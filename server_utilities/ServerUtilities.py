import RPi.GPIO as GPIO

def GoForward(pin_set:tuple):
    '''
    Function to go forward --> on press: w
    '''
    leftMotorEnable, rightMotorEnable ,leftPinForward, leftPinBackward, rightPinForward, rightPinBackward = pin_set
    GPIO.output(leftPinForward, GPIO.HIGH)
    GPIO.output(leftPinBackward, GPIO.LOW)
    GPIO.output(rightPinForward, GPIO.HIGH)
    GPIO.output(rightPinBackward, GPIO.LOW)
    print("[+] Going Forward")

def GoBackward(pin_set:tuple):
    '''
    Function to go backward --> on press: s
    '''
    leftMotorEnable, rightMotorEnable ,leftPinForward, leftPinBackward, rightPinForward, rightPinBackward = pin_set
    GPIO.output(leftPinForward, GPIO.LOW)
    GPIO.output(leftPinBackward, GPIO.HIGH)
    GPIO.output(rightPinForward, GPIO.LOW)
    GPIO.output(rightPinBackward, GPIO.HIGH)
    print("[+] Going Backward")


def GoLeft(pin_set:tuple):
    '''
    Function to turn left --> on press: a
    '''
    leftMotorEnable, rightMotorEnable ,leftPinForward, leftPinBackward, rightPinForward, rightPinBackward = pin_set
    GPIO.output(leftPinForward, GPIO.LOW)
    GPIO.output(leftPinBackward, GPIO.HIGH)
    GPIO.output(rightPinForward, GPIO.HIGH)
    GPIO.output(rightPinBackward, GPIO.LOW)
    print("[+] Going left")

def GoRight(pin_set:tuple):
    '''
    Function to go right --> on press: d
    '''
    leftMotorEnable, rightMotorEnable ,leftPinForward, leftPinBackward, rightPinForward, rightPinBackward = pin_set
    GPIO.output(leftPinForward, GPIO.HIGH)
    GPIO.output(leftPinBackward, GPIO.LOW)
    GPIO.output(rightPinForward, GPIO.LOW)
    GPIO.output(rightPinBackward, GPIO.HIGH)
    print("[+] Turning Right")

def Stop(pin_set:tuple):
    '''
    Function to stop the bot --> on release: all keys
    '''
    leftMotorEnable, rightMotorEnable ,leftPinForward, leftPinBackward, rightPinForward, rightPinBackward = pin_set
    GPIO.output(leftPinForward, GPIO.LOW)
    GPIO.output(leftPinBackward, GPIO.LOW)
    GPIO.output(rightPinForward, GPIO.LOW)
    GPIO.output(rightPinBackward, GPIO.LOW)
    print("[+] Bot Stopped")

def Quit(pin_set:tuple):
    '''
    Function to quit the controls
    '''
    leftMotorEnable, rightMotorEnable ,leftPinForward, leftPinBackward, rightPinForward, rightPinBackward = pin_set
    GPIO.output(leftPinForward, GPIO.LOW)
    GPIO.output(leftPinBackward, GPIO.LOW)
    GPIO.output(rightPinForward, GPIO.LOW)
    GPIO.output(rightPinBackward, GPIO.LOW)
    GPIO.output(leftMotorEnable, GPIO.LOW)
    GPIO.output(rightMotorEnable, GPIO.LOW)
    print("[+] Quitting")