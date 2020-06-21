from struct import pack, unpack
import sys
import os
import socket
from inputs import get_gamepad, devices
from time import sleep
import _thread

keys = {
    "A": 1,
    "B": 1 << 1,
    "X": 1 << 2,
    "Y": 1 << 3,
    "LST": 1 << 4,
    "RST": 1 << 5,
    "L": 1 << 6,
    "R": 1 << 7,
    "ZL": 1 << 8,
    "ZR": 1 << 9,
    "PLUS": 1 << 10,
    "MINUS": 1 << 11,
    "DL": 1 << 12,
    "DU": 1 << 13,
    "DR": 1 << 14,
    "DD": 1 << 15,
    "LL": 1 << 16,
    "LU": 1 << 17,
    "LR": 1 << 18,
    "LD": 1 << 19,
    "RL": 1 << 20,
    "RU": 1 << 21,
    "RR": 1 << 22,
    "RD": 1 << 23
}


def set_del_bit(bit, status, out):
    if status:
        out |= bit
    else:
        out &= ~bit
    return out


def check_keys(key, status, out):

    # for i in range(13):
    #     print(joystick.get_button(i))
    # print("--")

    if key == "BTN_NORTH":
        out = set_del_bit(keys["X"], status, out)
    if key == "BTN_EAST":
        out = set_del_bit(keys["A"], status, out)
    if key == "BTN_SOUTH":
        out = set_del_bit(keys["B"], status, out)
    if key == "BTN_WEST":
        out = set_del_bit(keys["Y"], status, out)

    if key == "BTN_DPAD_UP":
        out = set_del_bit(keys["DU"], status, out)
    if key == "BTN_DPAD_RIGHT":
        out = set_del_bit(keys["DR"], status, out)
    if key == "BTN_DPAD_DOWN":
        out = set_del_bit(keys["DD"], status, out)
    if key == "BTN_DPAD_LEFT":
        out = set_del_bit(keys["DL"], status, out)

    if key == "BTN_TL":
        out = set_del_bit(keys["L"], status, out)
    if key == "BTN_TR":
        out = set_del_bit(keys["R"], status, out)

    if key == "BTN_TL2":
        out = set_del_bit(keys["ZL"], status, out)
    if key == "BTN_TR2":
        out = set_del_bit(keys["ZR"], status, out)

    if key == "BTN_THUMBL":
        out = set_del_bit(keys["LST"], status, out)
    if key == "BTN_THUMBR":
        out = set_del_bit(keys["RST"], status, out)

    if key == "BTN_START":
        out = set_del_bit(keys["MINUS"], status, out)
    if key == "BTN_SELECT":
        out = set_del_bit(keys["PLUS"], status, out)

    return out


def print_in(buttons):
    for name, bm in keys.items():
        if buttons & bm:
            print(name, end=" ")
    print("")


if len(sys.argv) != 2:
    print("Usage: python3 input_pc.py SWITCH_IP")
    os._exit(1)

print("welcome!")  
server_address = (sys.argv[1], 8000)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# -------- Main Program Loop -----------

#P1
keyout = 0
dx_l = 0
dy_l = 0
dx_r = 0
dy_r = 0

#P2
twoKeyout = 0
twoDx_l = 0
twoDy_l = 0
twoDx_r = 0
twoDy_r = 0

#P3
threeKeyout = 0
threeDx_l = 0
threeDy_l = 0
threeDx_r = 0
threeDy_r = 0

#P4
fourKeyout = 0
fourDx_l = 0
fourDy_l = 0
fourDx_r = 0
fourDy_r = 0

if len(devices.gamepads) == 0:
    print("No gamepads found")
    os._exit(1)

controllerCount = len(devices.gamepads)

gamepad_type = str(devices.gamepads[0])

class myGamepad(object):
    keys = 0
    dx_l = 0
    dy_l = 0
    dx_r = 0
    dy_r = 0
    id = 5
    pad = devices.gamepads[0]

print("welcome!")
gamepadList = []
for i in range(0, 7):
    tempCon = myGamepad()
    tempCon.id = i
    if i < controllerCount:
        tempCon.pad = devices.gamepads[i]
    gamepadList.append(tempCon)
    print(gamepadList[i].id, " (", gamepadList[i].pad, ")")


print(gamepad_type, "Controllers connected:", controllerCount)
def input_poller():
    global keyout
    global dx_l
    global dy_l
    global dx_r
    global dy_r
    usedGamepad = gamepadList[0]
    while(True):
        print(usedGamepad.id, " READING...")
        try:
            events = usedGamepad.pad.read()
        except:
            print("Gamepad disconnected")
            os._exit(1)

        for event in events:
            if event.ev_type == "Key":
                keyout = check_keys(event.code, event.state, keyout)
            elif event.ev_type == "Absolute":
                if(event.code == "ABS_X"):
                    if gamepad_type == "Sony PLAYSTATION(R)3 Controller":
                        dx_l = (event.state-128) * 255
                    else:
                        dx_l = event.state
                    if(abs(dx_l) < 5000):
                        dx_l = 0
                if(event.code == "ABS_Y"):
                    if gamepad_type == "Sony PLAYSTATION(R)3 Controller":
                        dy_l = -(event.state-128) * 255
                    else:
                        dy_l = -event.state
                    if(abs(dy_l) < 5000):
                        dy_l = 0
                if(event.code == "ABS_RX"):
                    if gamepad_type == "Sony PLAYSTATION(R)3 Controller":
                        dx_r = (event.state-128) * 255
                    else:
                        dx_r = event.state
                    if(abs(dx_r) < 5000):
                        dx_r = 0
                if(event.code == "ABS_RY"):
                    if gamepad_type == "Sony PLAYSTATION(R)3 Controller":
                        dy_r = -(event.state-128) * 255
                    else:
                        dy_r = -event.state
                    if(abs(dy_r) < 5000):
                        dy_r = 0
                if gamepad_type != "Sony PLAYSTATION(R)3 Controller":
                    if(event.code == "ABS_Z"):
                        if event.state >= 100:
                            keyout = check_keys("BTN_TL2", 1, keyout)
                        else:
                            keyout = check_keys("BTN_TL2", 0, keyout)
                    if(event.code == "ABS_RZ"):
                        if event.state >= 100:
                            keyout = check_keys("BTN_TR2", 1, keyout)
                        else:
                            keyout = check_keys("BTN_TR2", 0, keyout)
                    if(event.code == "ABS_HAT0X"):
                        if event.state == 0:
                            keyout = check_keys("BTN_DPAD_LEFT", 0, keyout)
                            keyout = check_keys("BTN_DPAD_RIGHT", 0, keyout)
                        if event.state == 1:
                            keyout = check_keys("BTN_DPAD_RIGHT", 1, keyout)
                        if event.state == -1:
                            keyout = check_keys("BTN_DPAD_LEFT", 1, keyout)
                    if(event.code == "ABS_HAT0Y"):
                        if event.state == 0:
                            keyout = check_keys("BTN_DPAD_UP", 0, keyout)
                            keyout = check_keys("BTN_DPAD_DOWN", 0, keyout)
                        if event.state == 1:
                            keyout = check_keys("BTN_DPAD_DOWN", 1, keyout)
                        if event.state == -1:
                            keyout = check_keys("BTN_DPAD_UP", 1, keyout)

        usedGamepad.keys = keyout
        usedGamepad.dx_l = dx_l
        usedGamepad.dx_r = dx_r
        usedGamepad.dy_l = dy_l
        usedGamepad.dy_r = dy_r

def inputTwo_poller():
    global twoKeyout
    global twoDx_l
    global twoDy_l
    global twoDx_r
    global twoDy_r
    usedGamepad = gamepadList[1]
    if controllerCount < 2:
        usedGamepad.keys = 0
        usedGamepad.dx_l = 0
        usedGamepad.dx_r = 0
        usedGamepad.dy_l = 0
        usedGamepad.dy_r = 0
    if controllerCount >= 2:
        while(True):
            print(usedGamepad.id, " READING...")
            try:
                events = usedGamepad.pad.read()
            except:
                print("Gamepad disconnected, using defaults...")
                usedGamepad.keys = 0
                usedGamepad.dx_l = 0
                usedGamepad.dx_r = 0
                usedGamepad.dy_l = 0
                usedGamepad.dy_r = 0
            if controllerCount >= 2:
                for event in events:
                    if event.ev_type == "Key":
                        twoKeyout = check_keys(event.code, event.state, twoKeyout)
                    elif event.ev_type == "Absolute":
                        if(event.code == "ABS_X"):
                            if gamepad_type == "Sony PLAYSTATION(R)3 Controller":
                                twoDx_l = (event.state-128) * 255
                            else:
                                twoDx_l = event.state
                            if(abs(twoDx_l) < 5000):
                                twoDx_l = 0
                        if(event.code == "ABS_Y"):
                            if gamepad_type == "Sony PLAYSTATION(R)3 Controller":
                                twoDy_l = -(event.state-128) * 255
                            else:
                                twoDy_l = -event.state
                            if(abs(twoDy_l) < 5000):
                                twoDy_l = 0
                        if(event.code == "ABS_RX"):
                            if gamepad_type == "Sony PLAYSTATION(R)3 Controller":
                                twoDx_r = (event.state-128) * 255
                            else:
                                twoDx_r = event.state
                            if(abs(twoDx_r) < 5000):
                                twoDx_r = 0
                        if(event.code == "ABS_RY"):
                            if gamepad_type == "Sony PLAYSTATION(R)3 Controller":
                                twoDy_r = -(event.state-128) * 255
                            else:
                                twoDy_r = -event.state
                            if(abs(twoDy_r) < 5000):
                                twoDy_r = 0
                        if gamepad_type != "Sony PLAYSTATION(R)3 Controller":
                            if(event.code == "ABS_Z"):
                                if event.state >= 100:
                                    twoKeyout = check_keys("BTN_TL2", 1, twoKeyout)
                                else:
                                    twoKeyout = check_keys("BTN_TL2", 0, twoKeyout)
                            if(event.code == "ABS_RZ"):
                                if event.state >= 100:
                                    twoKeyout = check_keys("BTN_TR2", 1, twoKeyout)
                                else:
                                    twoKeyout = check_keys("BTN_TR2", 0, twoKeyout)
                            if(event.code == "ABS_HAT0X"):
                                if event.state == 0:
                                    twoKeyout = check_keys("BTN_DPAD_LEFT", 0, twoKeyout)
                                    twoKeyout = check_keys("BTN_DPAD_RIGHT", 0, twoKeyout)
                                if event.state == 1:
                                    twoKeyout = check_keys("BTN_DPAD_RIGHT", 1, twoKeyout)
                                if event.state == -1:
                                    twoKeyout = check_keys("BTN_DPAD_LEFT", 1, twoKeyout)
                            if(event.code == "ABS_HAT0Y"):
                                if event.state == 0:
                                    twoKeyout = check_keys("BTN_DPAD_UP", 0, twoKeyout)
                                    twoKeyout = check_keys("BTN_DPAD_DOWN", 0, twoKeyout)
                                if event.state == 1:
                                    twoKeyout = check_keys("BTN_DPAD_DOWN", 1, twoKeyout)
                                if event.state == -1:
                                    twoKeyout = check_keys("BTN_DPAD_UP", 1, twoKeyout)

                usedGamepad.keys = twoKeyout
                usedGamepad.dx_l = twoDx_l
                usedGamepad.dx_r = twoDx_r
                usedGamepad.dy_l = twoDy_l
                usedGamepad.dy_r = twoDy_r

def inputThree_poller():
    global threeKeyout
    global threeDx_l
    global threeDy_l
    global threeDx_r
    global threeDy_r
    usedGamepad = gamepadList[2]
    if controllerCount < 3:
        usedGamepad.keys = 0
        usedGamepad.dx_l = 0
        usedGamepad.dx_r = 0
        usedGamepad.dy_l = 0
        usedGamepad.dy_r = 0
    if controllerCount >= 3:
        print("CONTROLLER COUNT: ", controllerCount)
        while(True):
            print(usedGamepad.id, " READING...")
            try:
                events = usedGamepad.pad.read()
            except:
                print("Gamepad disconnected, using defaults...")
                usedGamepad.keys = 0
                usedGamepad.dx_l = 0
                usedGamepad.dx_r = 0
                usedGamepad.dy_l = 0
                usedGamepad.dy_r = 0
            for event in events:
                if event.ev_type == "Key":
                    threeKeyout = check_keys(event.code, event.state, threeKeyout)
                elif event.ev_type == "Absolute":
                    if(event.code == "ABS_X"):
                        if gamepad_type == "Sony PLAYSTATION(R)3 Controller":
                            threeDx_l = (event.state-128) * 255
                        else:
                            threeDx_l = event.state
                        if(abs(threeDx_l) < 5000):
                            threeDx_l = 0
                    if(event.code == "ABS_Y"):
                        if gamepad_type == "Sony PLAYSTATION(R)3 Controller":
                            threeDy_l = -(event.state-128) * 255
                        else:
                            threeDy_l = -event.state
                        if(abs(threeDy_l) < 5000):
                            threeDy_l = 0
                    if(event.code == "ABS_RX"):
                        if gamepad_type == "Sony PLAYSTATION(R)3 Controller":
                            threeDx_r = (event.state-128) * 255
                        else:
                            threeDx_r = event.state
                        if(abs(threeDx_r) < 5000):
                            threeDx_r = 0
                    if(event.code == "ABS_RY"):
                        if gamepad_type == "Sony PLAYSTATION(R)3 Controller":
                            threeDy_r = -(event.state-128) * 255
                        else:
                            threeDy_r = -event.state
                        if(abs(threeDy_r) < 5000):
                            threeDy_r = 0
                    if gamepad_type != "Sony PLAYSTATION(R)3 Controller":
                        if(event.code == "ABS_Z"):
                            if event.state >= 100:
                                threeKeyout = check_keys("BTN_TL2", 1, threeKeyout)
                            else:
                                threeKeyout = check_keys("BTN_TL2", 0, threeKeyout)
                        if(event.code == "ABS_RZ"):
                            if event.state >= 100:
                                threeKeyout = check_keys("BTN_TR2", 1, threeKeyout)
                            else:
                                threeKeyout = check_keys("BTN_TR2", 0, threeKeyout)
                        if(event.code == "ABS_HAT0X"):
                            if event.state == 0:
                                threeKeyout = check_keys("BTN_DPAD_LEFT", 0, threeKeyout)
                                threeKeyout = check_keys("BTN_DPAD_RIGHT", 0, threeKeyout)
                            if event.state == 1:
                                threeKeyout = check_keys("BTN_DPAD_RIGHT", 1, threeKeyout)
                            if event.state == -1:
                                threeKeyout = check_keys("BTN_DPAD_LEFT", 1, threeKeyout)
                        if(event.code == "ABS_HAT0Y"):
                            if event.state == 0:
                                threeKeyout = check_keys("BTN_DPAD_UP", 0, threeKeyout)
                                threeKeyout = check_keys("BTN_DPAD_DOWN", 0, threeKeyout)
                            if event.state == 1:
                                threeKeyout = check_keys("BTN_DPAD_DOWN", 1, threeKeyout)
                            if event.state == -1:
                                threeKeyout = check_keys("BTN_DPAD_UP", 1, threeKeyout)

                usedGamepad.keys = threeKeyout
                usedGamepad.dx_l = threeDx_l
                usedGamepad.dx_r = threeDx_r
                usedGamepad.dy_l = threeDy_l
                usedGamepad.dy_r = threeDy_r


def inputFour_poller():
    global fourKeyout
    global fourDx_l
    global fourDy_l
    global fourDx_r
    global fourDy_r
    usedGamepad = gamepadList[3]
    if controllerCount < 4:
        usedGamepad.keys = 0
        usedGamepad.dx_l = 0
        usedGamepad.dx_r = 0
        usedGamepad.dy_l = 0
        usedGamepad.dy_r = 0
    if controllerCount >= 4:
        while(True):
            print(usedGamepad.id, " READING...")
            try:
                events = usedGamepad.pad.read()
            except:
                print("Gamepad disconnected, using defaults...")
                usedGamepad.keys = 0
                usedGamepad.dx_l = 0
                usedGamepad.dx_r = 0
                usedGamepad.dy_l = 0
                usedGamepad.dy_r = 0
            if controllerCount <= 4:
                for event in events:
                    if event.ev_type == "Key":
                        fourKeyout = check_keys(event.code, event.state, fourKeyout)
                    elif event.ev_type == "Absolute":
                        if(event.code == "ABS_X"):
                            if gamepad_type == "Sony PLAYSTATION(R)3 Controller":
                                fourDx_l = (event.state-128) * 255
                            else:
                                fourDx_l = event.state
                            if(abs(fourDx_l) < 5000):
                                fourDx_l = 0
                        if(event.code == "ABS_Y"):
                            if gamepad_type == "Sony PLAYSTATION(R)3 Controller":
                                fourDy_l = -(event.state-128) * 255
                            else:
                                fourDy_l = -event.state
                            if(abs(fourDy_l) < 5000):
                                fourDy_l = 0
                        if(event.code == "ABS_RX"):
                            if gamepad_type == "Sony PLAYSTATION(R)3 Controller":
                                fourDx_r = (event.state-128) * 255
                            else:
                                fourDx_r = event.state
                            if(abs(fourDx_r) < 5000):
                                fourDx_r = 0
                        if(event.code == "ABS_RY"):
                            if gamepad_type == "Sony PLAYSTATION(R)3 Controller":
                                fourDy_r = -(event.state-128) * 255
                            else:
                                fourDy_r = -event.state
                            if(abs(fourDy_r) < 5000):
                                fourDy_r = 0
                        if gamepad_type != "Sony PLAYSTATION(R)3 Controller":
                            if(event.code == "ABS_Z"):
                                if event.state >= 100:
                                    fourKeyout = check_keys("BTN_TL2", 1, fourKeyout)
                                else:
                                    fourKeyout = check_keys("BTN_TL2", 0, fourKeyout)
                            if(event.code == "ABS_RZ"):
                                if event.state >= 100:
                                    fourKeyout = check_keys("BTN_TR2", 1, fourKeyout)
                                else:
                                    fourKeyout = check_keys("BTN_TR2", 0, fourKeyout)
                            if(event.code == "ABS_HAT0X"):
                                if event.state == 0:
                                    fourKeyout = check_keys("BTN_DPAD_LEFT", 0, fourKeyout)
                                    fourKeyout = check_keys("BTN_DPAD_RIGHT", 0, fourKeyout)
                                if event.state == 1:
                                    fourKeyout = check_keys("BTN_DPAD_RIGHT", 1, fourKeyout)
                                if event.state == -1:
                                    fourKeyout = check_keys("BTN_DPAD_LEFT", 1, fourKeyout)
                            if(event.code == "ABS_HAT0Y"):
                                if event.state == 0:
                                    fourKeyout = check_keys("BTN_DPAD_UP", 0, fourKeyout)
                                    fourKeyout = check_keys("BTN_DPAD_DOWN", 0, fourKeyout)
                                if event.state == 1:
                                    fourKeyout = check_keys("BTN_DPAD_DOWN", 1, fourKeyout)
                                if event.state == -1:
                                    fourKeyout = check_keys("BTN_DPAD_UP", 1, fourKeyout)

                usedGamepad.keys = fourKeyout
                usedGamepad.dx_l = fourDx_l
                usedGamepad.dx_r = fourDx_r
                usedGamepad.dy_l = fourDy_l
                usedGamepad.dy_r = fourDy_r


_thread.start_new_thread(input_poller, ())
_thread.start_new_thread(inputTwo_poller, ())
_thread.start_new_thread(inputThree_poller, ())
_thread.start_new_thread(inputFour_poller, ())



while(True):
    #print(event.ev_type, event.code, event.state)
    #print(keyout)
    #
    
    #INPUTS!                                    MAGIC-  KEYS FROM GAMEPAD 1  AMOUNT OF CONS-  STICKS FROM GAMEPAD 1---------------------------------------------------------------  KEYS FROM GAMEPAD 2  STICKS FROM GAMEPAD 2---------------------------------------------------------------  KEYS FROM GAMEPAD 3  STICKS FROM GAMEPAD 3---------------------------------------------------------------  KEYS FROM GAMEPAD 4  STICKS FROM GAMEPAD 4---------------------------------------------------------------
    #sock.sendto(pack("<HQHiiiiQiiiiQiiiiQiiii", 0x3275, gamepadList[0].keys, controllerCount, gamepadList[0].dx_l, -gamepadList[0].dy_l, gamepadList[0].dx_r, -gamepadList[0].dy_r, gamepadList[1].keys, gamepadList[1].dx_l, -gamepadList[1].dy_l, gamepadList[1].dx_r, -gamepadList[1].dy_r, gamepadList[2].keys, gamepadList[2].dx_l, -gamepadList[2].dy_l, gamepadList[2].dx_r, -gamepadList[2].dy_r, gamepadList[3].keys, gamepadList[3].dx_l, -gamepadList[3].dy_l, gamepadList[3].dx_r, -gamepadList[3].dy_r), server_address)
    sock.sendto(pack("<HQiiii", 0x3275, gamepadList[0].keys, gamepadList[0].dx_l, -gamepadList[0].dy_l, gamepadList[0].dx_r, -gamepadList[0].dy_r), server_address)
    print("P1: ", gamepadList[0].keys, " P2: ", gamepadList[1].keys, " P3: ", gamepadList[2].keys, " P4: ", gamepadList[3].keys)
    sleep(1/60)
