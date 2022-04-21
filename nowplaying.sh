#!/bin/bash

if [ $(playerctl status) = 'Playing' ]; then
    a=$( playerctl metadata artist )
    t=$( playerctl metadata title )
    echo "$a - $t"
fi

exit 0
