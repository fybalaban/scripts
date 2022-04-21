#!/bin/bash
if [ $(playerctl status) = 'Playing' ]; then
    echo $( playerctl -f '{{trunc(xesam:artist, 20)}} - {{trunc(xesam:title, 30)}}' metadata )
fi
exit 0
