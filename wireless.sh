#!/usr/bin/env bash
#
#     Yigid BALABAN, <fyb@fybx.dev>
#

control() {
    local device="$1"
    local subcommand="$2"

    case "$subcommand" in
        off)
            rfkill block "$device" &&

            case $device in
                bluetooth) bluetoothctl power off ;;
                wifi) nmcli radio wifi off ;;
            esac
            ;;
        on)

            rfkill unblock "$device" && sleep 1 &&

            case $device in
                bluetooth) bluetoothctl power on ;;
                wifi) nmcli radio wifi on ;;
            esac
            ;;
        *)
            # shellcheck disable=SC2154
            echo "$command: subcommand '$subcommand' is not a valid argument." >&2
            return 1
    esac
}

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <device> <subcommand>" >&2
    echo "Valid devices: bluetooth, wifi" >&2
    echo "Valid subcommands: on, off" >&2
    exit 1
fi

control "$1" "$2"
