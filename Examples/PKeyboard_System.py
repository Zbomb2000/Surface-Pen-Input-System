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

print("/------------------------------- Welcome to Pen Keyboard System v1.0 -------------------------------\\")
print("|                                                                                                   |")
print("| This is an early beta release. Please send feedback to 27MaritatoL@fenwickfalcons.org. Thank you! |")
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
print("2: backspace/exit (send twice)")
print("3: tab/enter")
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

a_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']
current_index = 0

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("[RECEIVED] %s" % message)

    #  Do some 'work'
    time.sleep(0.1)

    if message == b'input1' or message == b'input2':
        exitclicks = 0

    if message == b'input3':
        # exitclicks += 1
        if exitclicks == 3:
            # print("[SERVER] Hold-click 2 more times to exit")
            pass
        if exitclicks == 4:
            # print("[SERVER] Hold-click 1 more time to exit")
            pass
        if exitclicks == 5:
            # print("[SERVER] Exiting...")
            # sys.exit() disabled
            pass

    if input_shift == 1 and not cyclevar:
        if message == b'input1':
            if current_index >= 26:
                current_index = 0
            else:
                current_index += 1
            print()
            print("Current letter: '"+a_list[current_index]+"'")

        if message == b'input3':
            keyboard.write(a_list[current_index])

        if message == b'input2':
            input_shift = 2
            print("Shifted input to backspace/exit")
            cyclevar = True

    if input_shift == 2 and not cyclevar:
        if message == b'input3':
            exitclicks += 1
            if exitclicks == 1:
                print()
                print("[SERVER] Hold-click 1 more time to exit.")
            elif exitclicks >= 2:
                print()
                print("[SERVER] Shutting down...")
                sys.exit()

        if message == b'input2':
            input_shift = 3
            print("Shifted input to tab/enter")
            cyclevar = True
            exitclicks = 0

        if message == b'input1':
            keyboard.press("backspace")
            print()
            print("Sent backspace.")

    if input_shift == 3 and not cyclevar:
        if message == b'input3':
            keyboard.press("enter")
            print()
            print("Sent enter.")

        if message == b'input2':
            input_shift = 1
            print("Shifted input to switch/type")
            cyclevar = True

        if message == b'input1':
            keyboard.press("tab")
            print()
            print("Sent tab.")

    #  Send reply back to client
    socket.send(b"World")
    cyclevar = False
