'''
Raspberry Pi side of the code
Functions as the server socket and does all the moving of the servos
'''
import RPi.GPIO as GPIO
import time
import numpy as np
import socket
import struct
import select
# Define the socket
server_socket = socket.socket()
server_socket.bind(('', 9000))  # Binds socket to a given port. Port must be the same for the connection to succeed. 
clientIP = "xx.x.x.xxx"  # IP Address of desired client (input it here)
server_socket.listen(5)
print("Socket is listening")
while True:
    c, addr = server_socket.accept()
    try:
        if addr[0] == clientIP:
            print("Got connection from desired IP")
            break
        else:
            print("Undesired IP connecting")
            destroy()
            break
    except ValueError:
        pass
OFFSE_DUTY = 0.5  # Define pulse offset of servo
SERVO_MIN_DUTY = 2.5+OFFSE_DUTY  # Define pulse duty cycle for minimum angle of servo
SERVO_MAX_DUTY = 12.5+OFFSE_DUTY  # Define pulse duty cycle for maximum angle of servo
servoPin = 12  # Setting pin for servo under camera
servo2Pin = 11  # Setting pin for servo that's mimicking the other


def map(value, fromLow, fromHigh, toLow, toHigh):
    return (toHigh-toLow)*(value-fromLow) / (fromHigh-fromLow) + toLow


def setup():  # Initializing servos
    global p
    global pm
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(servoPin, GPIO.OUT)
    GPIO.output(servoPin, GPIO.LOW)
    GPIO.setup(servo2Pin, GPIO.OUT)
    GPIO.output(servo2Pin, GPIO.LOW)
    p = GPIO.PWM(servoPin, 50)  # Set frequency to 50 Hz
    pm = GPIO.PWM(servo2Pin, 50)
    p.start(0)
    pm.start(0)

  
def servoWrite(angle, p_num):  # Makw one of the two servos rotate to a specific angle, 0 to 180
    if (angle<0):
        angle = 0
    elif (angle>180):
        angle = 180
    if p_num == 1:
        p.ChangeDutyCycle(map(angle,0,180,SERVO_MIN_DUTY,SERVO_MAX_DUTY))  # Map the angle to duty cycle and output it
    else:
        pm.ChangeDutyCycle(map(angle,0,180,SERVO_MIN_DUTY,SERVO_MAX_DUTY))  # Map the angle to duty cycle and output it


def loop():  # RPi looping code. Stop the code on the RPi to properly stop code on computer. 
    episod = 0  # Defines parameters
    batch_size = 50
    while True:
        ang = np.random.randint(0, 18)
        ang = ang*10
        for dc in range(0, ang+1, 1):
            servoWrite(dc,1)
            time.sleep(0.001)
        c.send((str(ang)).encode())
        time.sleep(1)  # So computer has enough time for screenshot
        for dc in range(ang, -1, -1):
            servoWrite(dc,1)
            time.sleep(0.001)
        episod += 1
        if episod % (2*batch_size) == 0:
            while True:  # pauses until model finishes fitting
                data = c.recv(4)
                myint = decode(dat)
                try:
                    if myint == '1':
                        break
                except ValueError:
                    pass
            if episode % (batch_size*10) == 0:
                ang = np.rand.randint(0,18)
                ang = ang*10
                for dc in range(0, ang+1, 1):
                    servoWrite(dc,1)
                    time.sleep(0.001)
                time.sleep(1)  # To give it enough time to predict
                for dc in range(ang, -1, -1):
                    servoWrite(dc,1)
                    time.sleep(0.001)
                time.sleep(0.125)
                data = c.recv(1024)
                predang = int(decode(data))
                for dc in range(0, predang+1, 1):
                    servoWrite(dc,0)
                    time.sleep(0.001)
                time.sleep(0.5)
                for dc in range(predang, -1, -1):
                    servoWrite(dc,0)
                    time.sleep(0.001)
        time.sleep(1)  # To give space between episodes
    
    
def destroy():
    p.stop()
    pm.stop()
    GPIO.cleanup()
    server_socket.close()
  
  
if __name__ == '__main__':
    print('Program is starting...')
    setup()
    try:
        with c:
            loop()
  except KeyboardInterrupt:
      destroy()
    
