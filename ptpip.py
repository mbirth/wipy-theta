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

    def getSocket(self):
        return self.socket

    def initCommand(self, guid, identifier):
        pkg = self.createPkg(1, str.encode(guid[:16]) + str.encode(identifier))
        self.socket.send(pkg)
        result = self.recvPkg()
        return result
