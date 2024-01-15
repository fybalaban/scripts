#!/usr/bin/env bash
#
#     Ferit Yiğit BALABAN,      <fyb@fybx.dev>
#     change_hyprland_mode.sh,  2024
#

path_mode="$HOME/.config/navi/power_mode"
dir_hypr="$HOME/.config/hypr"
path_save="$dir_hypr/hyprland.s.conf"
path_normal="$dir_hypr/hyprland.n.conf"
target="$dir_hypr/hyprland.conf"

powersave() {
  cp "$path_save" "$target"
  echo "powersave" > "$path_mode"
}

performance() {
  cp "$path_normal" "$target"
  echo "performance" > "$path_mode"
}

if [ "$1" == "save" ]; then
  powersave
elif [ "$1" == "normal" ]; then
  performance
else
  current=$(cat "$path_mode")
  if [ "$current" == "powersave" ]; then
    performance
  else
    powersave
  fi
fi

