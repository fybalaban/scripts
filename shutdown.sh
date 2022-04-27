#!/bin/bash
dt=$(date +'%d/%m/%y-%H.%M.%S')
echo "[$dt] navi shutting down..." >> navi.log
brightnessctl set 128
brightnessctl --device asus::kbd_backlight 1
shutdown -h now
