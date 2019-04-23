from network import Sigfox
import socket
import struct
import pycom

# init Sigfox for RCZ1 (Europe)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)

# create a Sigfox socket
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

# make the socket blocking
s.setblocking(True)
s.settimeout(60)


def change_led(v):
    if v is None:
        return
    vi = struct.unpack('>L', v[-4:])[0]
    pycom.rgbled(vi)


def send_and_receive(msg):
    # configure it as both ways link
    s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, True)
    try:
        s.send(msg)
    except OSError as e:
        print('error in send...', e)
    else:
        response = s.recv(64)
        change_led(response)
        return response


def send(msg):
    # configure it uplink only
    s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)
    return s.send(msg)


# stop led heartbeat
pycom.heartbeat(False)


