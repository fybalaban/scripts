#!/usr/bin/env bash

mac=$(cat .maclist)

bluetoothctl connect "$mac"

if [ $? -eq 0 ]; then
  pactl set-default-sink "bluez_output.$(tr : _ <<< $mac).1"
fi
