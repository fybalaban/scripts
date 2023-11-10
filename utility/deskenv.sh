#!/usr/bin/env bash
#
#       Ferit Yiğit BALABAN,        <fybalaban@fybx>
#       desktop environment timer,  2023
#

NIGHT_START="18:00"
DAY_START="9:30"
MODE_FILE="$HOME/.config/navi/desktop_mode"

night=$(awk -F: '{print $1 * 60 + $2}' <<< "$NIGHT_START")
day=$(awk -F: '{print $1 * 60 + $2}' <<< "$DAY_START")

current_time=$(awk -F: '{print $1 * 60 + $2}' <<< "$(date +%H:%M)")
current_dir=$(dirname "${BASH_SOURCE[0]}")

isDaytime() {
    if ((current_time >= day && current_time < night)); then
        return 0
    else
        return 1
    fi
};

runForDay() {
    echo "It's day time. Running day time script."
    bash "$current_dir/run_at_day.sh" "$pass"
    echo "day" > "$MODE_FILE"
}

runForNight() {
    echo "It's night time. Running night time script."
    bash "$current_dir/run_at_night.sh" "$pass"
    echo "dark" > "$MODE_FILE"
}

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
