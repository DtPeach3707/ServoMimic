# ServoMimic Summary
My first Raspberry Pi Machine Learning using sockets to have a computer do the computationally expensive parts. <br>
The computer functions as the client socket and the Raspberry Pi (RPi) functions as the server socket. <br>
The computer takes a screenshot of video feed from a USB camera directly over the servo when it has fully turned out and the RPi sends the computer the angle of the servo, which is randomized.<br>
It eventually learns what images correspond to each angle and every certain episodes a testing cycle is done where the servo under the camera turns then the computer sends its predicted angle to the RPi to turn the second servo.

# How to get it working
- Have all the libraries used in the code for each device installed on their respective devices (most should be preinstalled, except for Tensorflow or PIL)
- Have a servo motor fastened or stuck down somewhere to where when the RPi sends a signal for it to move it doesn't move the rest of the part and where a USB camera can have constant feed of it.  
- Wire the RPi correctly (will be shown in a diagram soon once the PCB website I'm using is no longer down for maintenance).
- Run the code on the RPi first, wait until the RPi prints out "Socket is listening"
- Start running the code on the computer, and then it should start learning

If you wish to terminate the code, stop it running on the RPi side, and eventually the code on the computer will quit automatically due to not recieving any tangible data. It will save the model you have if you wish to load it in for more testing cycles. 
