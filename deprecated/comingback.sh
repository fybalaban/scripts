#!/usr/bin/env bash
#
#       Ferit Yigit BALABAN <fyb@duck.com>, 2022
#

# Step 1: Revert status from default location
screen=$(cat $HOME/.config/navi/screen)
kbdlgt=$(cat $HOME/.config/navi/kbdlgt)
brightnessctl set $screen
brightnessctl set --device asus::kbd_backlight $kbdlgt

# Step 2: Set mouse light to breathing colors
rivalcfg --color=#FF66F5 --light-effect=breath

# Step 3: Write log message
dt=$(date +'%d/%m/%y-%H.%M.%S')
echo "[$dt] navi was unlocked. fyb's back!" >> $HOME/navi.log