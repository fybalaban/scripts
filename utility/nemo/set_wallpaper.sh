#!/usr/bin/env bash
#
#       Ferit Yiğit BALABAN,        <fyb@fybx.dev>
#       desktop environment utility 2023
# 

# ln ~/scripts/utility/nemo/set_wallpaper.sh ~/.local/share/nemo/scripts

mode=$(cat "$HOME/.config/navi/desktop_mode")
first=$(echo "$NEMO_SCRIPT_SELECTED_FILE_PATHS" | head -n 1)
bgl="$HOME/.config/navi/img_background_light"
bgd="$HOME/.config/navi/img_background_dark"

if [ "$mode" = "light" ]; then
  cp "$first" "$bgl"
else
  cp "$first" "$bgd"
fi

bash "$HOME/scripts/utility/deskenv.sh" nobright "$mode"
