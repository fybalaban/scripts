#!/usr/bin/env bash
#
#       Ferit Yiğit BALABAN,        <fyb@fybx.dev>
#       desktop environment,        2024
#

BASE="$HOME/.config/navi"
NIGHT_START="17:00"
DAY_START="09:30"
MODE_FILE="$BASE/desktop_mode"
LOG="$BASE/deskenv.log"
FIREFOX="$HOME/.mozilla/firefox/pb8ar5xe.default-release/chrome"

night=$(awk -F: '{print $1 * 60 + $2}' <<< "$NIGHT_START")
day=$(awk -F: '{print $1 * 60 + $2}' <<< "$DAY_START")
current_time=$(awk -F: '{print $1 * 60 + $2}' <<< "$(date +%H:%M)")
current_dir=$(dirname "${BASH_SOURCE[0]}")

file_w="$BASE/img_background"
file_wl="$BASE/img_background_light"
file_wd="$BASE/img_background_dark"

mkdirs() {
    mkdir -p "$BASE"
}

isDaytime() {
    if ((current_time >= day && current_time < night)); then
        return 0
    else
        return 1
    fi
};

setWallpaperSwww() {
    types=("left" "right" "top" "bottom" "wipe" "wave" "grow" "outer")
    ltypes=${#types[@]}
    rindex=$((RANDOM % ltypes))
    rtype=${types[rindex]}

    swww img --transition-type "$rtype" --transition-pos 1,1 --transition-step 90 "$file_w"
}

runForDay() {
    echo "It's day time. Running day time script."
    echo "light" > "$MODE_FILE"
    cp "$file_wl" "$file_w"
    cp "$FIREFOX/userChrome.l.css" "$FIREFOX/userChrome.css"
    setWallpaperSwww
    
    bash "$HOME/scripts/chores/kitty.sh" light
    # wal --backend haishoku -nqei "$file_wl" >/dev/null 2>"$LOG"

    gsettings set org.gnome.desktop.interface gtk-theme "RosePine-Main-BL"
    gsettings set org.gnome.desktop.interface color-scheme 'prefer-light'
    bash "$current_dir/toggle_vscode_theme.sh" light

    if [ "$pass" != "nobright" ]; then
        brightnessctl -qd 'asus::kbd_backlight' set 0
        brightnessctl -q set 35%
    fi
}

runForNight() {
    echo "It's night time. Running night time script."
    echo "dark" > "$MODE_FILE"
    cp "$file_wd" "$file_w"
    cp "$FIREFOX/userChrome.d.css" "$FIREFOX/userChrome.css"
    setWallpaperSwww
    
    bash "$HOME/scripts/chores/kitty.sh" dark
    # wal --backend haishoku -nqei "$file_wd" >/dev/null 2>"$LOG"

    gsettings set org.gnome.desktop.interface gtk-theme 'RosePine-Main-BL'
    gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'
    bash "$current_dir/toggle_vscode_theme.sh" dark

    if [ "$pass" != "nobright" ]; then
        brightnessctl -qd 'asus::kbd_backlight' set 33%
        brightnessctl -q set 10%
    fi
}

mkdirs
wal -c 2> "$LOG"

if ! [ "$1" == "nobright" ]; then
    pass="normal"
else
    pass="nobright"
fi

if [ "$2" == "dark" ]; then
    runForNight 
elif [ "$2" == "light" ]; then
    runForDay
elif [ "$2" == "toggle" ]; then
    last_mode=$(cat "$MODE_FILE")
    if [ "$last_mode" == "dark" ]; then
        runForDay
    else
        runForNight
    fi
else
    if isDaytime; then
        runForDay
    else
        runForNight
    fi
fi

bash "$current_dir/change_hyprland_borders.sh"
