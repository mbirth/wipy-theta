"""
PTP/IP class for MicroPython
@author Markus Birth <markus@birth-online.de>
"""
import socket
import struct

class PTPIP:
    def __init__(self, ipadr):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ipadr, 15740))
        self.socket.setblocking(1)    # wait for answer

    def createPkg(self, pktype, payload):
        pklen = len(payload) + 8
        pkg = struct.pack('<I', pklen) + struct.pack('<I', pktype) + payload
        return pkg

    def recvPkg(self):
        pklen = self.socket.recv(4)
        pklen_int = struct.unpack('<I', pklen)[0]
        print("Incoming: %i bytes" % pklen_int)
        pktype = self.socket.recv(4)
        pktype_int = struct.unpack('<I', pktype)[0]
        print("Packet type: %i" % pktype_int)
        payload = self.socket.recv(pklen_int - 8)
        return (pktype_int, payload)

    # see http://www.ietf.org/rfc/rfc2781.txt
    def utf16to8(self, u16text):
        u8text = ""
        for i in range(0, len(u16text), 2):
            char16 = u16text[i:i+2]
            char16 = struct.unpack('<H', char16)[0]
            if char16 < 0xd800 or char16 > 0xdfff:
                u8text += chr(char16)
            else:
                print("Encoded UTF-16. Please improve this method.")
        return u8text

    # see http://www.ietf.org/rfc/rfc2781.txt
    def utf8to16(self, u8text):
        pass

    def getSocket(self):
        return self.socket

    def initCommand(self, guid, identifier):
        pkg = self.createPkg(1, str.encode(guid[:16]) + str.encode(identifier))
        self.socket.send(pkg)
        result = self.recvPkg()
        if result[0] == 5:
            print("INIT FAILED!")
            return False
        elif result[0] != 2:
            print("Unknown package type: %i" % result[0])
            return False
        remote_guid = result[1][0:16]
        remote_name = self.utf16to8(result[1][16:])
        return (remote_guid, remote_name)
