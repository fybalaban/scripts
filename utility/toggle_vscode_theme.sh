#!/usr/bin/env bash
#
#       Ferit Yiğit BALABAN,    <fybalaban@fybx>
#       toggle_vscode_theme.sh, 2023
#

path_settings="$HOME/.config/Code/User/settings.json"
preferred_dark=$(grep -o '"workbench.preferredDarkColorTheme": *"[^"]*"' < "$path_settings" | cut -d '"' -f4)
preferred_light=$(grep -o '"workbench.preferredLightColorTheme": *"[^"]*"' < "$path_settings" | cut -d '"' -f4)

if ! command -v code &> /dev/null; then
    echo "VS Code is not installed. Please install it and try again."
    exit 1
fi

case $1 in
    'light' | l)
        sed -i "s/\"workbench.colorTheme\": \"[^\"]*\"/\"workbench.colorTheme\": \"$preferred_light\"/" "$path_settings";;
    'dark' | d)
        sed -i "s/\"workbench.colorTheme\": \"[^\"]*\"/\"workbench.colorTheme\": \"$preferred_dark\"/" "$path_settings";;
    *)
        echo "Invalid argument. Please provide either 'light' or 'dark'."
        exit 1;;
esac