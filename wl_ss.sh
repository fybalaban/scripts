#!/usr/bin/env bash
#
#       Ferit Yiğit BALABAN, <fybalaban@fybx.dev>
#
#       Select an area with slurp, ss with grim 
#       and copy to clipboard.
export GRIM_DEFAULT_DIR="$HOME/shoka/swap/screenshots"
grim -g "$( slurp )" - | wl-copy --type image/png
