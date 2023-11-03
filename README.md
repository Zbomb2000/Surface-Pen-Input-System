# Surface-Pen-Input-System
Translates surface pen button clicks to input readable by Python.

## INSTRUCTIONS
1. Download the pinput1, 2, and 3 ```.pyw``` files from ```/Input-Files```

2. Make each file a shortcut
   - Open "File Explorer"
   - Go to the folder where you downloaded the "pinput" (pen input) files
   - Right click on one of the files
   - Click "Create shortcut"
   - Do that for the other two pinput files

3. Open "Settings > Devices > Pen and Windows Ink", and scroll down to "Pen Shortcuts"

4. For each option (Click once, Double click, Press and hold), do the following:
   - Choose the option "Launch a classic app"
   - Click "Browse"
   - Navigate to the folder with the pinput shortcut files
   - Select the respective input file for each click method

5. **You're all set up!** Write a script to process inputs, or use one from /Examples.

## How to write a input processor
Now you have inputs, but how do you actually use them? Here is a basic example of how to read input from the pen.
```
import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    message = socket.recv()
    print("[RECEIVED] %s" % message)

    time.sleep(0.1)

    if message == b'input1':
        print("Single-click recieved!")
    if message == b'input2':
        print("Double-click recieved!")
    if message == b'input3':
        print("Hold-click recieved!")

    socket.send(b"World")
```
**WOAH, THAT'S COOL! But what does it do?** Lets break this script down:
 - ```import zmq``` and ```import time``` - ```zmq``` is required to send messages between scripts (if not already installed, run ```pip install zmq```), and ```time``` is required for a short delay in the main loop.
  
 - ```context = zmq.Context()``` to ```socket.bind("tcp://*:5555")``` - Starts listing for input on port 5555 from the pinput scripts.
  
 - ```while True:``` and ```time.sleep(0.1)``` - This is the main loop that checks for input. It doesn't work without a short delay. Don't ask me, I don't know why. I copied some of this code from stackoverflow.

 - ```message = socket.recv()``` - Reads messages sent on port 5555 (pen inputs)

 - The ```if``` statements - Checks for inputs sent, you can customize these to fit your needs. Replace the ```print``` statements with whatever you need.

 - ```socket.send(b"World")``` - Sends "World" back to the input scripts so they know the input was recieved.

## Input Processor Examples
There are example input processors in the [/Examples](https://github.com/Zbomb2000/Surface-Pen-Input-System/tree/main/Examples) folder.

## Additional information
If you have any problems, you can submit an Isuse under the issues tab.
