#!/usr/bin/env bash
#
#       Ferit Yigit BALABAN <fyb@duck.com>, 2022
#

# Step 1: Set screen brightness to 0
brightnessctl set 0

# Step 2: Set keyboard backlight to 0
brightnessctl --device asus::kbd_backlight set 0

# Step 3: Set mouse light to 0
rivalcfg --color=#000000 --light-effect=steady

# Step 4: Set volume level to 0
pactl set-sink-volume @DEFAULT_SINK@ 0%

# Step 5: Lock the screen with screensaver
betterlockscreen --lock --off 10
