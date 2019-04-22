import socket
import struct
from network import LoRa
import pycom
from machine import Timer

# A basic package header, B: 1 byte for the deviceId, B: 1 byte for the pkg size, %ds: Formatted string for string
_LORA_PKG_FORMAT = "!BB%ds"
# A basic ack package, B: 1 byte for the deviceId, B: 1 byte for the pkg size, B: 1 byte for the Ok (200) or error messages
_LORA_PKG_ACK_FORMAT = "BBB"

# Open a LoRa Socket, use rx_iq to avoid listening to our own messages
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORA, rx_iq=True, region=LoRa.EU868)
lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

this_device_id = 1


def handle_timer(timer):
    print('handle timer...')
    pycom.heartbeat(True)


def handle_pkg(recv_pkg):
    try:
        if len(recv_pkg) > 2:
            recv_pkg_len = recv_pkg[1]
            print('received: (%d/%d) %r' % (
                recv_pkg_len, len(recv_pkg) - 2, recv_pkg))

            device_id, pkg_len, msg = struct.unpack(_LORA_PKG_FORMAT % recv_pkg_len, recv_pkg)
            print('Device: %d - Pkg:  %s' % (device_id, msg))

            pycom.heartbeat(False)
            if device_id == this_device_id:
                if pkg_len == 6:
                    pycom.rgbled(int(msg, 16))
                    result = 200
                else:
                    pycom.rgbled(0x00ff00)
                    result = 210
            ack_pkg = struct.pack(_LORA_PKG_ACK_FORMAT, device_id, 1, result)
            lora_sock.send(ack_pkg)
        else:
            pycom.rgbled(0xffd400)
    except Exception as e:
        print('Error in handle_pkg: ', e)
        try:
            pycom.rgbled(0xff0000)
        except Exception as ee:
            print('Error in error...', ee)
    finally:
        Timer.Alarm(handle_timer, 10)
    print('end handle_pkg')


def sync_rec():
    print('starting sync_rec')
    lora_sock.setblocking(True)
    while True:
        recv_pkg = lora_sock.recv(512)
        if recv_pkg:
            print('lora packet received')
            handle_pkg(recv_pkg)
    print('end sync_rec - we should not see this message...')


def handle_rec(lora):
    print('handle_rec: %r' % lora)
    event = lora.events()
    print('  event: ', event)
    if event & LoRa.RX_PACKET_EVENT:
        print('lora packed received')
        recv_pkg = lora_sock.recv(256)
        handle_pkg(recv_pkg)
    elif event & LoRa.TX_PACKET_EVENT:
        print('lora packet sent - we should never see this message')
    print('end of handle_rec')


def async_rec():
    print('starting async_rec')
    lora_sock.setblocking(False)
    lora.callback(trigger=LoRa.RX_PACKET_EVENT, handler=handle_rec)
    print('receive handler connected, waiting for packets...')
    print('exiting async_rec')
