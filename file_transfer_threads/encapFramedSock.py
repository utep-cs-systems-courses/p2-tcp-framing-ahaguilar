

import re

class EncapFramedSock:
    def __init__(self, sockAddress):
        self.sock, self.address = sockAddress
        self.rbuf = b""  # receive the buffer

    def close(self):
        return self.sock.close()

    def send(self, fileName, payload):
        msg = str(len(payload)).encode() + b':' + fileName.encode() + b':' + payload

        while len(msg):
            nsent = self.sock.send(msg)
            msg = msg[nsent:]

    def receive(self):
        state = "getLength"
        msgLength = -1

        while True:
            if state == "getLength":
                match = re.match(b'([^:]+):(.*):(.*)', self.rbuf, re.DOTALL | re.MULTILINE)
                if match:
                    print("match ********")
                    lengthStr, fileName, self.rbuf = match.groups()
                    try:
                        msgLength = int(lengthStr)
                    except:
                        if len(self.rbuf):
                            print("bad message length:", lengthStr)
                            return None, None
                    state = "getPayload"
            if state == "getPayload":
                print ("checking*******")
                if len(self.rbuf) >= msgLength:
                    payload = self.rbuf[0:msgLength]
                    self.rbuf = self.rbuf[msgLength:]
                    return fileName, payload
            print("receiving ******")
            r = self.sock.recv(100)
            self.rbuf += r
            print("adding to buff ***********")

            if len(r) == 0:
                print("empty *********")
                if len(self.rbuf) != 0:
                    print("FramedReceive: incomplete message. \n state=%s, length=%d, self.                            rbuf=%s" % (state, msgLength, self.rbuf))
                return None, None

    def sendStatus(self, status):
        self.sock.sendall(str(status).encode())

    def Status(self):
        status = self.sock.recv(128)
        return status                          
