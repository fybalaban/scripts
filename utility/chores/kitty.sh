#!/usr/bin/env bash
#
# 	Yigid BALABAN, 			<fyb@fybx.dev>
# 	reve desktop environment	2024
#

# Chore:
# Set kitty theme according to given argument.
# Accepted args: d/dark l/light

KITTY="$HOME/.config/kitty"

case $1 in
	'l' | 'light')
		kitty +kitten themes --reload-in=all Rosé Pine Dawn ;;	
	'd' | 'dark')
		kitty +kitten themes --reload-in=all Rosé Pine Moon ;;
	*)
		echo "Invalid argument. This chore accepts 'l/light' or 'd/dark'" ;;
esac
