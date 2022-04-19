#!/usr/bin/env python3
import os.path
import subprocess
import sys


def main():
    primary_color = '#c38ccf'
    prc_frmstring = f'F{primary_color}'
    prc_fwrappers = f'{{{prc_frmstring}}}'
    backg_colour = '#0f0f14'
    backg_clralt = '#0f0f14'
    foreg_colour = '#FFEBFF'

    interface_wlan = 'wlp3s0'
    interface_ethr = 'enp2s0'

    config_text = f"""[colors]
    background = {backg_colour}
    background-alt = {backg_clralt}
    foreground = {foreg_colour}
    primary = {primary_color}
    secondary = ${{colors.primary}}
    alert = #A54242
    disabled = #707880
    
    [bar/example]
    width = 100%
    height = 2.5%
    radius = 0
    font-0 = "JetBrainsMono Nerd Font;2"
    font-1 = "IPAGothic"

    background = ${{colors.background}}
    foreground = ${{colors.foreground}}
    
    line-size = 0
    border-size = 0
    border-color = ${{colors.primary}}
    
    padding-left = 0
    padding-right = 1
    module-margin = 1
    
    separator = |
    separator-foreground = ${{colors.disabled}}
    modules-left = xworkspaces music
    modules-center = arch xwindow
    modules-right = aud bat mem cpu temp wlan eth date
    cursor-click = pointer
    enable-ipc = true
   
    [module/music]
    type = custom/script
    exec = /home/ferit/scripts/nowplaying.py
    tail = true
    interval = 2

    [module/arch]
    type = custom/text
    content = " "
    content-foreground = {primary_color}
    
    [module/xworkspaces]
    type = internal/xworkspaces
    label-active = 
    label-active-foreground = ${{colors.primary}}
    label-active-background = ${{colors.background-alt}}
    label-active-underline= ${{colors.primary}}
    label-active-padding = 1
    
    label-occupied = 
    label-occupied-padding = 1
    
    label-urgent = ●
    label-urgent-background = ${{colors.alert}}
    label-urgent-padding = 1
    
    label-empty = ●
    label-empty-foreground = ${{colors.disabled}}
    label-empty-padding = 1
    
    [module/xwindow]
    type = internal/xwindow
    label = %title:0:31:...%
    
    [module/aud]
    type = internal/pulseaudio
    format-volume-prefix = " "
    format-volume-prefix-foreground = ${{colors.primary}}
    format-volume = <label-volume>
    label-volume = %percentage%%
    label-muted = 
    label-muted-foreground = ${{colors.disabled}}
    
    [module/bat]
    type = internal/battery
    full-at = 100
    battery = BAT0
    adapter = ADP0
    poll-interval = 5
    
    ramp-capacity-0 = 
    ramp-capacity-1 =  
    ramp-capacity-2 = 
    ramp-capacity-3 = 
    ramp-capacity-4 = 
    ramp-capacity-5 = 
    ramp-capacity-6 = 
    ramp-capacity-7 = 
    ramp-capacity-8 = 
    
    animation-charging-0 = 
    animation-charging-1 = 
    animation-charging-2 = 
    animation-charging-3 = 
    animation-charging-4 = 
    animation-charging-5 = 
    animation-charging-6 = 
    animation-charging-framerate = 750
    
    format-charging = %{prc_fwrappers}<animation-charging>%{{F-}} <label-charging>
    format-discharging = %{prc_fwrappers}<ramp-capacity>%{{F-}} <label-discharging>
    format-full = %{prc_fwrappers}%{{F-}} <label-full>
    label-full = %percentage%%
    label-charging = %percentage%%
    label-discharging = %percentage%%
    
    [module/mem]
    type = internal/memory
    interval = 2
    format-prefix = " "
    format-prefix-foreground = ${{colors.primary}}
    label = %percentage_used%%
    
    [module/cpu]
    type = internal/cpu
    interval = 2
    format-prefix = " "
    format-prefix-foreground = ${{colors.primary}}
    label = %percentage%%
    
    [module/temp]
    type = internal/temperature
    interval = 10
    thermal-zone = 0
    hwmon-path = /sys/class/hwmon/hwmon1/temp1_input
    format-prefix = "﨎 "
    format-prefix-foreground = ${{colors.primary}}
    label = %temperature-c%
    
    [module/wlan]
    type = internal/network
    interval = 5
    interface = {interface_wlan}
    label-connected = %essid%
    label-disconnected =
    format-connected = %{prc_fwrappers}直%{{F-}} <label-connected>
    format-disconnected = %{prc_fwrappers}睊%{{F-}} <label-disconnected>
    
    [module/eth]
    type = internal/network
    interval = 5
    interface = {interface_ethr}
    label-connected = UP
    label-disconnected =
    format-connected = %{prc_fwrappers}%{{F-}} <label-connected>
    format-disconnected = <label-disconnected>
    
    [module/date]
    type = internal/date
    interval = 60
    date = %H.%M
    date-alt = %d/%m/%y
    label = %date%
    label-foreground = ${{colors.primary}}
    
    [settings]
    screenchange-reload = true
    pseudo-transparency = true"""
    if 'source_polybar.py' in sys.argv:
        sys.argv.remove('source_polybar.py')
    sys.argv.reverse()
    location = ''
    lct_home = os.environ.get('HOME')
    flag_print = False
    flag_locset = False
    flag_deploy = False
    flag_restrt = False
    # flag_print: -p or --print
    # flag_locset: -l or --location followed by valid path to file or directory
    # flag_deploy: -d or --deploy
    while len(sys.argv) != 0:
        item = sys.argv.pop()
        flag_print = item == '-p' or item == '--print' or flag_print
        flag_deploy = item == '-d' or item == '--deploy' or flag_deploy
        flag_restrt = item == '-r' or item == '--restart' or flag_restrt
        if item == '-l' or item == '--location':
            if len(sys.argv) > 0:
                _ = sys.argv.pop()
                if os.path.isdir(_) and os.path.isfile(_) is False:
                    flag_locset = True
                    location = _
    if flag_print:
        print(config_text)
    if flag_deploy:
        with open(lct_home + '/.config/polybar/config.ini', 'w') as file:
            file.write(config_text)
        print('deployed config')
    if flag_restrt:
        process = subprocess.Popen(['sh', 'launch_polybar.sh'])
        _ = process.communicate()[0]
        print('restarted polybar')
    if flag_locset:
        with open(location, 'w') as file:
            file.write(config_text)
        print(f'saved config to {location}/config.ini')


main()
