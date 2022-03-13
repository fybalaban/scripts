#!/bin/bash
ps -C polybar >/dev/null && : || polybar --quiet --reload & disown
