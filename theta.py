"""
RICOH Theta class for MicroPython

@author Markus Birth <markus@birth-online.de>
"""

from network import WLAN
import ptpip

class Theta:

    def __init__(self):
        self.wlan = WLAN(WLAN.STA)
        pass

    def log(self, msg):
        print(msg)

    def findWifi(self):
        wlans = self.wlan.scan()
        for w in wlans:
            if w.ssid.startswith('THETA'):
                self.log('Found Theta WiFi: %s' % w.ssid)
                return w.ssid
        return False

    def connectWifi(self, ssid):
        password = ssid[-8:]
        return self.wlan.connect(ssid, auth=(WLAN.WPA, password))

    # convenience - might get removed
    def connect(self):
        wifi = self.findWifi()
        if not wifi:
            return False
        self.connectWifi(wifi)
        self.ptpip = ptpip.PTPIP('192.168.1.1')
        return self.ptpip

    def getPTPIP(self):
        return self.ptpip
