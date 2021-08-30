# ServoMimic Summary
My first Raspberry Pi Machine Learning using sockets to have a computer do the computationally expensive parts. <br>
The computer functions as the client socket and the Raspberry Pi (RPi) functions as the server socket. <br>
The computer takes a screenshot of video feed from a USB camera directly over the servo when it has fully turned out and the RPi sends the computer the angle of the servo, which is randomized.<br>
It eventually learns what images correspond to each angle and every certain episodes a testing cycle is done where the servo under the camera turns then the computer sends its predicted angle to the RPi to turn the second servo.
