'''
Code for computer (client socket)
Does all the computationally expensive parts so
the RPi doesn't have to.
Computer also has USB camera which grabs data
via screenshot when USB camera feed fills up the whole screen
So that is how it gets its image
Predicts angles from 0 to 180 in steps of 10
'''
import socket
from tensorflow.keras.layers import Dense, Input, Flatten, Conv2D, MaxPool2D
from PIL import ImageGrab
from tensorflow.keras.models import Model
import time
import numpy as np
import random
from tensorflow.keras.optimizers import Adam
import select
# Setting seed
time.sleep(3)  # To get to camera
np.random.seed(1)
random.seed(1)
# Defining the socket for the computer and port it will connect
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 9001  # Variable for port (has to be the same as the one your Pi connects to)
RPiIP = "10.0.0.129"  # Variable to put your Pi's IP Address
client_socket.connect((RPiIP, port))  # Connects to Raspberry Pi
# Defining get_screen function for USB Camera


def get_screen():  # Screenshot function
    screen = ImageGrab.grab(bbox=(200, 150, 1600, 1150))
    return screen


def forget(lis, ln):  # Forget function (to speed up training)
    for i in range(ln):
        lis.pop(0)


# Defining the neural network
inputs = Input(shape=(70, 96, 3))
result = Conv2D(128, (3, 3), activation='relu')(inputs)
result = Conv2D(64, (3, 3), activation='relu')(result)
result = MaxPool2D((2, 2))(result)
result = Conv2D(64, (3, 3), activation='relu')(result)
result = Conv2D(64, (3, 3), activation='relu')(result)
result = Conv2D(32, (2, 2), activation='relu')(result)
result = Flatten()(result)
result = Dense(128, activation='relu')(result)
result = Dense(64, activation='relu')(result)
result = Dense(64, activation='relu')(result)
result = Dense(64, activation='relu')(result)
result = Dense(1, activation='linear')(result)
angleModel = Model(inputs, result)
angleModel.compile(loss='mae', optimizer=Adam(), metrics=['accuracy'])  # Fun with Mean Absolute Error :)
print(angleModel.summary())
servo_img = []  # Defining storage lists and parameters
servo_ang = []
batch_size = 50
mov = 0
episode = 0
try:
    while 1:  # Infinite loop (stopping RPi program will break the loop)
        data = client_socket.recv(1024)  # Receives data from RPi for angle
        actang = float(data.decode())  # Decodes data and scales down
        servo_ang.append(actang/180)
        time.sleep(0.625)  # Gives enough time for motor to turn before screenshotting
        screen = np.array(get_screen().resize((96, 70)))
        servo_img.append(screen)
        mov += 1
        if mov == 2*batch_size:
            angleModel.fit(np.array(servo_img), np.array(servo_ang), batch_size=batch_size, epochs=1, verbose=True)
            client_socket.send(str(1).encode())  # Sends signal to RPi to tell it that computer is done.
            mov = 0
            episode += 1
            if episode % 5 == 0 and episode != 0:  # Validation run
                time.sleep(0.625)
                predimg = np.array(get_screen().resize((96, 70))).reshape((1, 70, 96, 3))  # Detects
                resang = float((angleModel.predict(predimg) * 18).squeeze())
                resang = round(resang) * 10  # Needs to be a whole number
                client_socket.send(str(resang).encode())  # Sends signal for angle it thinks the image is
        if mov > 20:  # Implementing forget function to speed up training
            forget(servo_img, batch_size)
            forget(servo_ang, batch_size)


except Exception as ex:  # Code will execute if program is stopped from RPi side
    print(ex)
    client_socket.close()
    angleModel.save_weights("AngleDetect.h5")  # Saves model
client_socket.close()
