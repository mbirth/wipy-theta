# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal

# Copy config.example.py to config.py and modify to your needs first!
import config
import machine

#from machine import UART
from os import dupterm
uart = machine.UART(0, 115200)
dupterm(uart)

if machine.reset_cause() != machine.SOFT_RESET:
    from network import WLAN
    wifi = WLAN()
    wifi.mode(WLAN.STA)
    ssids = wifi.scan()
    found = False
    for net in ssids:
        print("Checking %s" % net.ssid)
        if net.ssid == config.HOME_SSID:
            print("Found %s!" % net.ssid)
            wifi.connect(config.HOME_SSID, auth=(WLAN.WPA, config.HOME_PASSWORD))
            found = True
            break
    if not found:
        print("No eligible WiFi found.")
        wifi.mode(WLAN.AP)
