#!/usr/bin/env python3

import sys
import time
import os

import automationhat
time.sleep(0.1) # Short pause after ads1015 class creation recommended

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("""This example requires PIL.
Install with: sudo apt install python{v}-pil
""".format(v="" if sys.version_info.major == 2 else sys.version_info.major))
    sys.exit(1)

import ST7735 as ST7735

print("""input.py

This Automation HAT Mini example displays the status of
the three 24V-tolerant digital inputs.

Press CTRL+C to exit.
""")

# Create ST7735 LCD display class.
disp = ST7735.ST7735(
    port=0,
    cs=ST7735.BG_SPI_CS_FRONT,
    dc=9,
    backlight=25,
    rotation=270,
    spi_speed_hz=4000000
)

# Initialize display.
disp.begin()

on_colour = (99, 225, 162)
off_colour = (235, 102, 121)

# Values to keep everything aligned nicely.
on_x = 115
on_y = 35

off_x = 46
off_y = on_y

dia = 10
playIdx=3
fileIdx=0

def volumeUp():
    with open("/tmp/cmd.txt",'w') as tf:
        tf.write("volup\n")
        tf.write("quit\n")

    os.system("nc localhost 4212 < /tmp/cmd.txt")

def volumeDown():
    with open("/tmp/cmd.txt",'w') as tf:
        tf.write("voldown\n")
        tf.write("quit\n")

    os.system("nc localhost 4212 < /tmp/cmd.txt")

def initPlaylist():
    global files
    global fileIdx

    with open("/tmp/cmd.txt",'w') as tf:
        tf.write("add Videos/"+files[fileIdx]+"\n")
        tf.write("repeat on\n")
        tf.write("play\n")
        tf.write("quit\n")

    os.system("nc localhost 4212 < /tmp/cmd.txt")

def repeatOn():
    with open("/tmp/cmd.txt",'w') as tf:
        tf.write("repeat on\n")
        tf.write("quit\n")

    os.system("nc localhost 4212 < /tmp/cmd.txt")

def fullScreen():
    with open("/tmp/cmd.txt",'w') as tf:
        tf.write("f\n")
        tf.write("quit\n")

    os.system("nc localhost 4212 < /tmp/cmd.txt")

def playNext():
    global playIdx
    global fileIdx

    with open("/tmp/cmd.txt",'w') as tf:
        tf.write("delete "+str(playIdx)+"\n")
        playIdx = playIdx+1

        fileIdx = (fileIdx+1) % len(files)
        print("Playing file "+files[fileIdx])

        tf.write("add Videos/"+files[fileIdx]+"\n")
        tf.write("repeat on\n")
        tf.write("quit\n")

    os.system("nc localhost 4212 < /tmp/cmd.txt")

def stop():
    with open("/tmp/cmd.txt",'w') as tf:
        tf.write("stop\n")
        tf.write("quit\n")

    os.system("nc localhost 4212 < /tmp/cmd.txt")

files = [f for f in os.listdir("/home/admin/Videos/") if f.endswith("mp4")]
files = sorted(files)
print("Available files ",files)
fileIdx=0
playIdx=3

os.system("killall vlc")
os.system("DISPLAY=:0 vlc -f --intf rc --rc-host localhost:4212 &");
time.sleep(2.0)

print("Initplaylist")
initPlaylist()
time.sleep(1.0)
print("Repeat on")
repeatOn()

print("Started");
while True:
    if automationhat.input[2].is_on():
        # volume up
        print("Volume up")
        volumeUp()
    if automationhat.input[0].is_on():
        # volume down
        print("Volume down")
        volumeDown()
    if automationhat.input[1].is_on():
        # play second video
        playNext()

    time.sleep(1.0)
