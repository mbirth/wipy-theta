# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal

# Copy config.example.py to config.py and modify to your needs first!
import config

from network import WLAN
wifi = WLAN(mode=WLAN.STA)
wifi.connect(config.HOME_SSID, auth=(WLAN.WPA, config.HOME_PASSWORD))

from machine import UART
from os import dupterm
uart = UART(0, 115200)
dupterm(uart)
