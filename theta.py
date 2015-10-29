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
        # TODO: Return all visible Thetas
        for w in wlans:
            if w.ssid.startswith('THETA'):
                self.log('Found Theta WiFi: %s' % w.ssid)
                # THETAXL12345678     = Theta (original model) - PTP/IP
                # THETAXN12345678     = Theta m15 - PTP/IP
                # THETAXS12345678.OSC = Theta S   - OSC
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

    def initPTP(self):
        answer = self.ptpip.initCommand('1234567812345678', 'WiPy')
        if not answer:
            print("Init failed!")
            return False
        (session_id, guid, name) = answer
        pass2 = self.ptpip.initEvent(session_id)
        if not pass2:
            print("Init stage 2 failed!")
            return False
        return (session_id, guid, name)

    def openSession(self):
        answer = self.ptpip.createCommand(0x1002, [])
        return answer

    def closeSession(self):
        answer = self.ptpip.createCommand(0x1003, [])
        return answer

    def shoot(self):
        answer = self.ptpip.createCommand(0x100e, [0x0, 0x0])
        return answer

    def getPTPIP(self):
        return self.ptpip
