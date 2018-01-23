#!/bin/bash
echo Initializing system
echo .
source /home/pi/.profile
echo .
workon cv
echo .
python3 /home/pi/projects/sw/camera-effects-rpi-sw2017/engine/start.py

python3
