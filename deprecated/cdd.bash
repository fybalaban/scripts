#!/usr/bin/env bash 
#
#       Ferit Yiğit BALABAN, <fybalaban@fybx.dev>
#
#       cd on steroids for Johnny.Decimal directories 

# Define the cdd function
cdd() {
  local input="$1"
  local folder="$(basename "$PWD")"

  if [[ "$input" =~ ^[0-9]{3}\.[0-9]{2}$ ]]; then
    cd "$HOME/shoka/*/*/$input *"
  elif [[ "$input" =~ ^[0-9]{3}$ ]]; then
    cd "$HOME/shoka/*/$input *"
  elif [[ "$input" =~ ^[0-9]{2}$ && "$folder" =~ ^[0-9]{3} ]]; then
    cd "$HOME/shoka/*/*/${folder:0:3}.$input *"
  else
    echo "Invalid input: $input"
  fi
}

# Use the cdd function with the input argument
cdd "$1"
