#!/bin/bash
echo Wait while system is initalizing
echo .
source ~/.profile
echo .
workon cv
echo . 
python3 /home/pi/projects/sw/camera-effects-rpi-sw2017/engine/start.py
python3
