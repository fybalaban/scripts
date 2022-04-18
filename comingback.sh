#!/usr/bin/env bash
#
#       Ferit Yigit BALABAN <fyb@duck.com>, 2022
#

# Step 1: Screen brightness back at %50
brightnessctl set 50%

# Step 2: Set keyboard backlight to %33
brightnessctl --device asus::kbd_backlight set 33%

# Step 3: Set mouse light to breathing colors
rivalcfg --color=#FF66F5 --light-effect=breath
