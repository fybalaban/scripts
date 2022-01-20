import os.path
import subprocess
import sys


def main():
    primary_color = '#FF93A0'
    prc_frmstring = f'F{primary_color}'
    prc_fwrappers = f'{{{prc_frmstring}}}'
    backg_colour = '#282A2E'
    backg_clralt = '#373B41'
    foreg_colour = '#C5C8C6'

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
    
    background = ${{colors.background}}
    foreground = ${{colors.foreground}}
    
    line-size = 0
    border-size = 0
    border-color = ${{colors.primary}}
    
    padding-left = 0
    padding-right = 1
    module-margin = 1
    
    separator =
    separator-foreground = ${{colors.disabled}}
    
    modules-left = xworkspaces xwindow
    modules-center = date
    modules-right = aud bat mem cpu temp wlan eth
    
    cursor-click = pointer
    cursor-scroll = ns-resize
    
    enable-ipc = true
    
    ; tray-position = right
    
    ; wm-restack = generic
    ; wm-restack = bspwm
    ; wm-restack = i3
    
    ; override-redirect = true
    
    [module/xworkspaces]
    type = internal/xworkspaces
    
    label-active = %name%
    label-active-background = ${{colors.background-alt}}
    label-active-underline= ${{colors.primary}}
    label-active-padding = 1
    
    label-occupied = %name%
    label-occupied-padding = 1
    
    label-urgent = %name%
    label-urgent-background = ${{colors.alert}}
    label-urgent-padding = 1
    
    label-empty = %name%
    label-empty-foreground = ${{colors.disabled}}
    label-empty-padding = 1
    
    [module/xwindow]
    type = internal/xwindow
    label = %title:0:30:...%
    
    [module/aud]
    type = internal/pulseaudio
    
    format-volume-prefix = "奔 "
    format-volume-prefix-foreground = ${{colors.primary}}
    format-volume = <label-volume>
    
    label-volume = %percentage%%
    label-muted = 婢
    label-muted-foreground = ${{colors.disabled}}
    
    [module/bat]
    type = internal/battery
    full-at = 100
    time-format = %H:%M
    
    ; Use the following command to list batteries and adapters:
    ; $ ls -1 /sys/class/power_supply/
    battery = BAT0
    adapter = ADP1
    poll-interval = 5
    
    format-charging = %{prc_fwrappers}<animation-charging>%{{F-}}  <label-charging>
    format-discharging = %{prc_fwrappers}<animation-discharging>%{{F-}}  <label-discharging>
    format-full = %{prc_fwrappers}<ramp-capacity>%{{F-}}  <label-full>
    
    label-charging = %percentage%%
    label-discharging = %percentage%%
    label-full = FULL
    
    ramp-capacity-0 = 
    ramp-capacity-1 = 
    ramp-capacity-2 = 
    ramp-capacity-3 = 
    ramp-capacity-4 = 
    
    animation-charging-0 = 
    animation-charging-1 = 
    animation-charging-2 = 
    animation-charging-3 = 
    animation-charging-4 = 
    animation-charging-framerate = 1000
    
    animation-discharging-0 = 
    animation-discharging-1 = 
    animation-discharging-2 = 
    animation-discharging-3 = 
    animation-discharging-4 = 
    animation-discharging-framerate = 1000
    
    [module/mem]
    type = internal/memory
    interval = 2
    format-prefix = "RAM "
    format-prefix-foreground = ${{colors.primary}}
    label = %percentage_used:2%%
    
    [module/cpu]
    type = internal/cpu
    interval = 2
    format-prefix = "CPU "
    format-prefix-foreground = ${{colors.primary}}
    label = %percentage:2%%
    
    [module/temp]
    type = internal/temperature
    interval = 10
    thermal-zone = 0
    hwmon-path = /sys/class/hwmon/hwmon1/temp1_input
    base-temperature = 20
    warn-temperature = 70
    format-prefix = "﨎 "
    format-prefix-foreground = ${{colors.primary}}
    label= %temperature-c%
    
    ; ramp-signal-0 = :o
    ; ramp-signal-1 = >:
    ; ramp-signal-2 = :/
    ; ramp-signal-3 = ^^
    ; ramp-signal-4 = :D
    ; ramp-signal-5 = :>
    
    [module/wlan]
    type = internal/network
    interval = 5
    interface = wlp3s0
    label-connected = %{prc_fwrappers}直%{{F-}} %essid% %signal%%
    label-disconnected =
    format-connected = <label-connected>
    format-disconnected = <label-disconnected>
    
    [module/eth]
    type = internal/network
    interval = 5
    interface = enp2s0
    label-connected = %{prc_fwrappers}囹%{{F-}} UP
    label-disconnected =
    format-connected = <label-connected>
    format-disconnected = <label-disconnected>
    
    [module/tthr]
    type = internal/network
    interval = 5
    interface = usb0
    label-connected = %{prc_fwrappers}臨%{{F-}} UP
    label-disconnected =
    format-connected = <label-connected>
    format-disconnected = <label-disconnected>
    
    [module/date]
    type = internal/date
    interval = 60
    date = %Y-%m-%d %H:%M
    label = %date%
    label-foreground = ${{colors.primary}}
    
    [settings]
    screenchange-reload = true
    pseudo-transparency = true"""
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
        flag_print = item == '-p' or item == '--print'
        flag_deploy = item == '-d' or item == '--deploy'
        flag_restrt = item == '-r' or item == '--restart'
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
