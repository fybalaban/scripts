#!/usr/bin/env python3
#
#       Ferit Yiğit BALABAN <f@fybx.dev>, 2022
#
from datetime import datetime as dt


START_NIGHT = "22.30"
START_DAY = "8.20"


def get_hour():
    if dt.now().minute == 0:
        return f"{dt.now().hour}.00"
    return f"{dt.now().hour}.{dt.now().minute}"


def get_hour_spec(hour_str = None):
    if hour_str != None:
        return (int(hour_str.split('.')[0]) * 60) + int(hour_str.split('.')[0])
    else:
        return (dt.now().hour * 60) + dt.now().minute


def get_mode():
    low = get_hour_spec(START_DAY)
    now = get_hour_spec()
    hgh = get_hour_spec(START_NIGHT)
    return 0 if low <= now and now < hgh else 1


def main():
    print("modeset2 by fyb")
    print(f"local machine time: {get_hour()}")
    print(f"current mode is: {get_mode()}")


if __name__ == '__main__':
    main()

