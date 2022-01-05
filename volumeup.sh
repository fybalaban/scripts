#!/bin/bash
current=$(pacmd dump-volumes | awk 'NR==1{print $8}' | sed 's/\%//')
[ $current -lt 200 ] && pactl set-sink-volume @DEFAULT_SINK@ +5%
