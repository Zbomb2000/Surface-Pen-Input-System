#
#   Pen input server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"input[1, 2, 3]" from client, replies with b"World"
#

import time
import zmq
import keyboard
import sys
import pyautogui

print("/--------------------------- Welcome to Pen Xbox Controller System v1.1 ---------------------------\\")
print("|                                                                                                   |")
print("|                Please send feedback to 27MaritatoL@fenwickfalcons.org. Thank you!                 |")
print("|                                                                                                   |")
print("\\---------------------------------------------------------------------------------------------------/")
print("\n")
print("Instructions:")
print(" P. input         Server      Desc.")
print(" - Single click   [input1]    First option")
print(" - Hold-click     [input3]    Second option")
print(" - Double click   [input2]    Switch input")
print("\n")
print("------------ INPUT INDEX ------------")
print()
print("1: switch/type")
print("2: backspace/enter")
print("3: tab/enter")
print("4: mousedown/mouseright")
print("5: mouseup/mouseleft")
print("6: mouseleftclick/mouserightclick")
print()
print("-------------------------------------")
print("\n")
print("[SERVER] Ready for input...")

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

exitclicks = 0

input_shift = 1

cyclevar = False

current_index = 0
a_list = ["w", "s", "a", "d"]

def holdKey(keyname):
    #timer = 0
    #while timer < 2:
    #    time.sleep(0.1)
    #    timer += 0.1
    pyautogui.keyDown(keyname)
    time.sleep(1)
    pyautogui.keyUp(keyname)

lookamount = 200

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("[RECEIVED] %s" % message)

    #  Do some 'work'
    time.sleep(0.1)

    if message == b'input1' or message == b'input2':
        exitclicks = 0

    # Go forward, backward, left, or right
    if input_shift == 1 and not cyclevar:
        if message == b'input3':
            if current_index >= 3:
                current_index = 0
            else:
                current_index += 1
            print()
            print("Current input: '"+a_list[current_index]+"'")

        if message == b'input1':
            if a_list[current_index] == "a":
                holdKey("a")
                print()
                print("Go left")
            
            if a_list[current_index] == "w":
                holdKey("w")
                print()
                print("Go up")
            
            if a_list[current_index] == "s":
                holdKey("s")
                print()
                print("Go down")
            
            if a_list[current_index] == "d":
                holdKey("d")
                print()
                print("Go right")

        if message == b'input2':
            input_shift = 2
            print("Shifted input to look/toggle")
            cyclevar = True

  # Look left and right
    if input_shift == 2 and not cyclevar:
        if message == b'input3':
            if current_index >= 3:
                current_index = 0
            else:
                current_index += 1
            print()
            print("Current input: '"+a_list[current_index]+"'")

        if message == b'input2':
            input_shift = 3
            print("Shifted input to shoot/jump")
            cyclevar = True
            exitclicks = 0

        if message == b'input1':
            if a_list[current_index] == "a":
                pyautogui.moveRel(-lookamount, 0, duration = 0.15)
                print()
                print("Mouse left")
            
            if a_list[current_index] == "w":
                pyautogui.moveRel(0, -lookamount, duration = 0.15)
                print()
                print("Mouse up")
            
            if a_list[current_index] == "s":
                pyautogui.moveRel(0, lookamount, duration = 0.15)
                print()
                print("Mouse down")
            
            if a_list[current_index] == "d":
                pyautogui.moveRel(lookamount, 0, duration = 0.15)
                print()
                print("Mouse right")

    if input_shift == 3 and not cyclevar:
        if message == b'input3':
            holdKey("space")
            print()
            print("Sent spacebar.")

        if message == b'input2':
            input_shift = 4
            print("Shifted input to reload/change weapon")
            cyclevar = True

        if message == b'input1':
            pyautogui.click(button='left')
            print()
            print("Left click")

    if input_shift == 4 and not cyclevar:
        if message == b'input1':
            keyboard.press("r")

        if message == b'input2':
            input_shift = 1
            print("Shifted input to move/toggle")
            cyclevar = True

        if message == b'input3':
            pass

    #  Send reply back to client
    socket.send(b"World")
    cyclevar = False