#!/usr/bin/env python3
import subprocess as s


def main():
    l = str(s.run(['playerctl', 'metadata'], capture_output=True, text=True).stdout).splitlines()
    if len(l) == 0:
        print('')
        exit(0)
    artist = ''
    title = ''
    s_artist = 'chromium xesam:artist'
    s_title = 'chromium xesam:title'
    for x in l:
        if s_artist in x:
            artist = x.split(s_artist)[1].strip()
        elif s_title in x:
            title = x.split(s_title)[1].strip()
            break
    print(f'{artist} - {title}')


if __name__ == '__main__':
    main()

