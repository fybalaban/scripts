#!/bin/bash
#
#       Ferit Yiğit BALABAN,        <fybalaban@fybx>
#       desktop environment timer,  2023
#

select="/home/ferit/shoka/500-599 pictures/502 landscape/cringe/light/wallhaven-gpz2g7.jpg"
wallpaper="$HOME/.config/navi/img_background_light"
current_dir=$(dirname "${BASH_SOURCE[0]}")

# Set GTK theme to light mode
gsettings set org.gnome.desktop.interface gtk-theme "WhiteSur-Light-blue"
gsettings set org.gnome.desktop.interface color-scheme 'prefer-light'
bash "$current_dir/toggle_vscode_theme.sh" light

# Set keyboard brightness to 0 if first launch, otherwise don't change
if [ "$1" != "nobright" ]; then
    brightnessctl -qd 'asus::kbd_backlight' set 0
fi

# Set screen backlight to 50% if first launch, otherwise don't change
if [ "$1" != "nobright" ]; then
    brightnessctl -q set 50%
fi

cp "$select" "$wallpaper"
hyprctl hyprpaper wallpaper "eDP-1, $wallpaper" >/dev/null
if hyprctl monitors | grep -q 'Monitor HDMI-A-1'; then
    hyprctl hyprpaper wallpaper "HDMI-A-1, $wallpaper" >/dev/null
fi

# change desktop background
# if pgrep "hyprpaper" > /dev/null
# then
#     killall hyprpaper && hyprpaper >/dev/null & disown
# else
#     hyprpaper >/dev/null & disown
# fi

# generate and set color scheme
wal -nqei "$select" >/dev/null
