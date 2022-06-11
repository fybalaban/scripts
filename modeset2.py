#!/usr/bin/env python3
#
#       Ferit Yiğit BALABAN <f@fybx.dev>, 2022
#
from datetime import datetime as dt
import sys


START_NIGHT = "22.30"
START_DAY = "8.20"


def get_hour():
    if 0 <= dt.now().minute and dt.now().minute <= 9:
        return f"{dt.now().hour}.0{dt.now().minute}"
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
    sys.argv.remove(sys.argv[0])
    sys.argv.reverse()
    if len(sys.argv) == 1:
        if sys.argv[0] == "--login":
            print("Login")
        elif sys.argv[0] == "--lock":
            print("Lock")
        elif sys.argv[0] == "--unlock":
            print("Unlock")
        elif sys.argv[0] == "--shutdown":
            print("Shutdown")
    elif len(sys.argv) == 0: 
        print("modeset2 by fyb")
        print(f"local machine time: {get_hour()}")
        print(f"current mode is: {get_mode()}")
        print("""Available options:
1. Login
2. Lock
3. Unlock
4. Shutdown""")
    else:
        print("Issuing more than 1 argument to modeset2 is not supported yet. Aborting...")
        exit(1)
    exit(0)


if __name__ == '__main__':
    main()

