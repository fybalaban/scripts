#!/usr/bin/bash
current_layout=$( hyprctl devices -j |
	jq -r '.keyboards[] | .layout' |
	head -n1 |
	cut -c1-2 |
	tr 'a-z' 'A-Z'
)

layout="us"

if [ $current_layout == "US" ]; then
	layout="tr"
fi

hyprctl keyword input:kb_layout $layout
notify-send --urgency=low --expire-time=1000 --icon="/media/yigid/share/shoka/pictures/506 icon packs/cp.png" "Keyboard layout changed" "You are now on $layout"

