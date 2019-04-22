import socket
import struct
from network import LoRa

# A basic package header, B: 1 byte for the deviceId, B: 1 byte for the pkg size
_LORA_PKG_FORMAT = "BB%ds"
_LORA_PKG_ACK_FORMAT = "BBB"
DEVICE_ID = 0x01

# Open a Lora Socket, use tx_iq to avoid listening to our own messages
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORA, tx_iq=True, region=LoRa.EU868)
lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
lora_sock.setblocking(False)


def handle_ack(_lora):
    print('handle_ack: %r' % _lora)
    event = _lora.events()
    print('  event: ', event)
    if event & LoRa.RX_PACKET_EVENT:
        print('lora packed received')
        recv_ack = lora_sock.recv(256)
        if len(recv_ack) > 0:
            device_id, pkg_len, ack = struct.unpack(_LORA_PKG_ACK_FORMAT, recv_ack)
            if device_id == DEVICE_ID:
                if ack == 200:
                    print("ACK")
                else:
                    print("Message Failed", ack)
    elif event & LoRa.TX_PACKET_EVENT:
        print('lora packet sent - we should never see this message')


lora.callback(trigger=LoRa.RX_PACKET_EVENT, handler=handle_ack)
print('receive handler connected')


while True:
    # Package send containing a simple string
    _input = input('color?')
    values = _input.split(' ')
    msg = values[0]
    if len(values) > 1:
        try:
            DEVICE_ID = int(values[1])
            print('changing DEVICE_ID to', DEVICE_ID)
        except:
            pass
    print('couleur: (%d) %r' % (len(msg), msg))
    if len(msg) == 0:
        break
    if len(msg) >= 6:
        pkg = struct.pack(_LORA_PKG_FORMAT % len(msg), DEVICE_ID, len(msg), msg)
        lora_sock.send(pkg)
    else:
        print('format: 123456 (hexa)')

print('The end...')
