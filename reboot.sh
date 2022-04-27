#!/usr/bin/env bash
dt=$(date +'%d/%m/%y-%H.%M.%S')
echo "[$dt] navi restarting..." >> $HOME/navi.log
brightnessctl --device amdgpu_bl1 set 128
brightnessctl --device asus::kbd_backlight 1
reboot
