"""
PTP/IP class for MicroPython
@author Markus Birth <markus@birth-online.de>
"""

# PTP/IP abstract: http://www.cipa.jp/ptp-ip/index_e.html
# PTP packet structure: http://www.gphoto.org/doc/ptpip.php
#                   and https://github.com/gphoto/libgphoto2/blob/master/camlibs/ptp2/PTPIP.TXT
# PTP example implementation in JavaScript: https://github.com/feklee/ptp.js
# PTP response codes: http://www.javased.com/?source_dir=cameraptp/src/main/java/ste/ptp/Response.java

import binascii
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
        print("UTF-16: %s" % u16text)
        u8text = u''
        for i in range(0, len(u16text), 2):
            char16 = u16text[i:i+2]
            char16 = struct.unpack('<H', char16)[0]
            if char16 == 0:
                continue
            elif char16 < 0xd800 or char16 > 0xdfff:
                u8text += chr(char16)
            else:
                # 2-word-char
                print("Encoded UTF-16. Please improve this method.")
        print("UTF- 8: %s" % u8text)
        return u8text

    # see http://www.ietf.org/rfc/rfc2781.txt
    def utf8to16(self, u8text):
        u16text = b''
        for i in range(0, len(u8text)):
            char8 = u8text[i]
            if ord(char8)<0x10000:
                u16text += struct.pack('<H', ord(char8))
            else:
                # 2-word-char
                print("Need wide UTF-16. Please improve this method.")
        return u16text

    def getSocket(self):
        return self.socket

    def initCommand(self, guid, identifier):
        pkg = self.createPkg(1, str.encode(guid[:16]) + self.utf8to16(identifier))
        self.socket.send(pkg)
        result = self.recvPkg()
        if result[0] == 5:
            print("INIT FAILED!")
            return False
        elif result[0] != 2:
            print("Unknown package type: %i" % result[0])
            return False
        self.session_id  = struct.unpack('<I', result[1][0:4])[0]
        remote_guid = binascii.hexlify(result[1][4:20])
        remote_name = self.utf16to8(result[1][20:])
        self.trans_id = 0
        return (self.session_id, remote_guid, remote_name)

    def initEvent(self, session_id):
        pkg = self.createPkg(3, struct.pack('<I', session_id))
        self.socket.send(pkg)
        result = self.recvPkg()
        if result[0] == 5:
            print("INIT EVENT FAILED!")
            return False
        elif result[0] != 4:
            print("Unknown package type: %i" % result[0])
            return False
        return True

    def createCommand(self, cmd_code, cmd_args):
        if type(cmd_args) is not list:
            print("Specify cmd_args as list!")
            return False
        self.trans_id += 1
        payload = b''
        payload += struct.pack('<IHI', 1, cmd_code, self.trans_id)
        for a in cmd_args:
            payload += struct.pack('<I', a)
        pkg = self.createPkg(6, payload)
        self.socket.send(pkg)
        result = self.recvPkg()
        if result[0] != 7:
            print("Answer package was of type: %i (%s)" % (result[0], result[1]))
            return False
        (response_code, trans_id) = struct.unpack('<HI', result[1][0:6])
        remainder = result[1][6:]
        args = []
        while len(remainder) > 0:
            args.append(struct.unpack('<I', remainder[:4]))
            remainder = remainder[4:]
        return (response_code, trans_id, args)
