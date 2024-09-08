#!/bin/bash
#
#     yigid balaban <fyb@fybx.dev>
#     fetchsh, fetch script alternative to neofetch
#     revision 1

f_mem_read() {
  local result="error reading memory"
  result=$(grep "$1" /proc/meminfo | sed "s/$1://g" | sed "s/kB//g" | xargs)
  echo "$result"
}

f_mem_format() {
  result=$(echo "$1" | awk '{$1/=1048576;printf "%.2fGiB\n",$1}')
  echo "$result"
}

f_color() {
  for token in "$@"; do
    tokens+=("\u001b[31m$token\u001b[0m")
  done

  echo -e "Hi ${tokens[0]}, welcome to ${tokens[1]}. I see that you're on ${tokens[2]},"
  echo -e "running with Linux ${tokens[3]}. You've ${tokens[4]} packages installed."
  echo -e "Your RAM usage is ${tokens[5]} / ${tokens[6]} and uptime is ${tokens[7]}."
}

raw_memt=$(f_mem_read 'MemTotal')
raw_mema=$(f_mem_read 'MemAvailable')

name=$(whoami)
hostname=$(uname -n)
distname='Arch GNU+Linux'
kernvers=$(uname -r)
packgcnt=$(pacman -Q | wc -l)
memtotal=$(f_mem_format "$raw_memt")
memfree=$(f_mem_format $((raw_memt - raw_mema)))
uptime=$(uptime -p | sed 's/up//g' | xargs)

f_color "$name" "$hostname" "$distname" "$kernvers" "$packgcnt" "$memfree" "$memtotal" "$uptime"
