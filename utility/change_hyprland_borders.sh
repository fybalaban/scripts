#!/usr/bin/env bash
#       Ferit Yiğit BALABAN,        <fybalaban@fybx>
#       desktop environment timer,  2023
#

hyprland_config="$HOME/.config/hypr/hyprland.conf"
wal_colors="$HOME/.cache/wal/colors"

line2=$(head -n 2 < "$wal_colors" | tail -n 1 | sed 's/#//')
line3=$(head -n 3 < "$wal_colors" | tail -n 1 | sed 's/#//')

sed -i "s/col.active_border =.*/col.active_border = rgb($line2) rgb($line3)/" "$hyprland_config"
