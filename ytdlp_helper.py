#!/usr/bin/env python3
# Helps me to download whole playlists or just one video, in any format I wish.
from subprocess import run


def yt_dlp(url: str, what: int, form: int, ):
    try:
        if what == 1 and form == 1:
            run(['yt-dlp', '-x', '--audio-format', "'mp3'", '--audio-quality', '0', f"'{url}'"])
        elif what == 1 and form == 2:
            run(['yt-dlp', '-S', "'ext'", f"'{url}'"])
        elif what == 2 and form == 1:
            run(['yt-dlp'])
    except FileNotFoundError:
        print("Are you sure that yt-dlp is installed?")


def main():
    print("Welcome to yt-dlp helper!\n")
    url = input("Would you be kind and share the URL of content you wish to download: ")

    print("Which format do you want the downloaded content be in?")
    print("1. mp3")
    print("2. mp4")
    form = int(input("Please make your selection: "))

    print("1. I want to download a video.")
    print("2. I want to download a playlist.")    
    if input("Please make your selection: ") == 1:
        print("Alright! Your download shall begin now: ")
        yt_dlp(url, 1, form)
    else:
        yt_dlp(url, 2, form)


if __name__ == '__main__':
    main()
