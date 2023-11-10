#!/usr/bin/env bash

mkdir -p "./$1"
cd "./$1" || echo "Failed to change directory to $1" && exit 1
yt-dlp -x --audio-format best --audio-quality 0 "$2"
