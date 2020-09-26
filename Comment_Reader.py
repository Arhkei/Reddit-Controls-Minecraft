import praw
from praw.models import MoreComments
import time
import ctypes
from pynput.mouse import Button, Controller as MouseController

w = 0x11
s = 0x1F
q = 0x10
e = 0x12
r = 0x13
t = 0x14
y = 0x15
u = 0x16
i = 0x17
o = 0x18
p = 0x19
a = 0x1E
d = 0x20
f = 0x21
g = 0x22
h = 0x23
j = 0x24
k = 0x25
l = 0x26
z = 0x2C
x = 0x2D
c = 0x2E
v = 0x2F
b = 0x30
n = 0x31
m = 0x32
num1 = 0x02
num2 = 0x03
num3 = 0x04
num4 = 0x05
num5 = 0x06
num6 = 0x07
num7 = 0x08
num8 = 0x09
num9 = 0x0A
num0 = 0x0B
slash = 0x35
space = 0x39
enter = 0x1C
shift = 0x2A
comma = 0x33
apostrophe = 0x28
period = 0x34
SendInput = ctypes.windll.user32.SendInput
mouse = MouseController()

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

reddit = praw.Reddit(user_agent='Comment Extraction',
                     client_id="", client_secret="")


def analyzeCommand(command):
    if command == "!forward":
        PressKey(w)
        time.sleep(1)
        ReleaseKey(w)
    elif command == "!backward":
        PressKey(s)
        time.sleep(1)
        ReleaseKey(s)
    elif command == "!left":
        PressKey(a)
        time.sleep(1)
        ReleaseKey(a)
    elif command == "!right":
        PressKey(d)
        time.sleep(1)
        ReleaseKey(d)
    elif command == "!jump":
        PressKey(space)
        time.sleep(1)
        ReleaseKey(space)
    elif command == "!respawn":
        mouse.position = (961,595)
        mouse.click(Button.left)
    elif "!mine(" in command:
        try:
            beg = command.find("(")
            end = command.find(")")
            timeToMine = int(command[int(beg)+1:int(end)])
            if timeToMine <= 15:
                mouse.press(Button.left)
                time.sleep(timeToMine)
                mouse.release(Button.left)
        except:
            pass
    elif command == "!inventory":
        PressKey(e)
        time.sleep(0.1)
        ReleaseKey(e)
    elif command == "!place":
        mouse.click(Button.right)
    elif "!hotbar(" in command:
        try:
            beg = command.find("(")
            end = command.find(")")
            pos = int(command[int(beg)+1:int(end)])
            if pos == 1:
                PressKey(num1)
                ReleaseKey(num1)
            elif pos == 2:
                PressKey(num2)
                ReleaseKey(num2)
            elif pos == 3:
                PressKey(num3)
                ReleaseKey(num3)
            elif pos == 4:
                PressKey(num4)
                ReleaseKey(num4)
            elif pos == 5:
                PressKey(num5)
                ReleaseKey(num5)
            elif pos == 6:
                PressKey(num6)
                ReleaseKey(num6)
            elif pos == 7:
                PressKey(num7)
                ReleaseKey(num7)
            elif pos == 8:
                PressKey(num8)
                ReleaseKey(num8)
            elif pos == 9:
                PressKey(num9)
                ReleaseKey(num9)
        except:
            pass

record = []

while True:
    time.sleep(1)
    submission = reddit.submission(id='')
    for comment in submission.comments:
        if comment.id in record:
            continue
        else:
            #print("Processing comment: " + comment.id)
            record.append(comment.id)
            command = comment.body
            print(command)
            analyzeCommand(command)
