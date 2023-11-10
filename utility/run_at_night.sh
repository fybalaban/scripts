#!/bin/bash
#
#       Ferit Yiğit BALABAN,        <fybalaban@fybx>
#       desktop environment timer,  2023
#

select="/home/ferit/shoka/500-599 pictures/wallpapers/wallhaven-vqd1yl.png"
wallpaper="$HOME/.config/navi/img_background_dark"
current_dir=$(dirname "${BASH_SOURCE[0]}")

# Set GTK theme to dark mode
gsettings set org.gnome.desktop.interface gtk-theme "WhiteSur-Dark-blue"
gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'
bash "$current_dir/toggle_vscode_theme.sh" dark

# Set keyboard brightness to 66% if first launch, otherwise don't change
if [ "$1" != "nobright" ]; then
    brightnessctl -qd 'asus::kbd_backlight' set 66%
fi

# Set screen backlight to 20% if first launch, otherwise don't change
if [ "$1" != "nobright" ]; then
    brightnessctl -q set 20%
fi

cp "$select" "$wallpaper"
hyprctl hyprpaper wallpaper "eDP-1, $wallpaper" >/dev/null
if hyprctl monitors | grep -q 'Monitor HDMI-A-1'; then
    hyprctl hyprpaper wallpaper "HDMI-A-1, $wallpaper" >/dev/null
fi

# generate and set color scheme
wal -nqei "$select" >/dev/null
