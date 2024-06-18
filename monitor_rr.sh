#!/usr/bin/env bash

if [[ $# -ne 2 ]]; then
	echo "Usage: $0 <monitor> <refresh_rate>" >&2
	echo "monitor: must be a display name"
	echo "refresh_rate: must be a number"
	exit 1
fi

case "$1" in
	eDP-1) hyprctl keyword monitor eDP-1,1920x1080@$2,1920x0,1 ;;
	HDMI-A-1) hyprctl keyword monitor HDMI-A-1,1920x1080@$2,0x0,1 ;;
	*) echo "Unrecognized monitor '$1'"
esac
