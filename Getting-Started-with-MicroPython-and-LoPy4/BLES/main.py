from network import Bluetooth

bluetooth = Bluetooth()
bluetooth.set_advertisement(name='LoPy', service_uuid=0x180F)

def conn_cb (bt_o):
    events = bt_o.events()
    if  events & Bluetooth.CLIENT_CONNECTED:
        print("Client connected")
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print("Client disconnected")

bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)

srv1 = bluetooth.service(uuid=0x180F, isprimary=True)
chr1 = srv1.characteristic(uuid=0x2A19, value='50')

srv2 = bluetooth.service(uuid=0x180A, isprimary=True)
chr2 = srv2.characteristic(uuid=0x2A29, value='name string')

bluetooth.advertise(True)


def char1_cb_handler(chr):
    events = chr.events()
    if  events & Bluetooth.CHAR_WRITE_EVENT:
        print("Write request on char1 with value = {}".format(chr.value()))
    else:
        print("Read request on char1 value = {}".format(chr.value()))

char1_cb = chr1.callback(trigger=Bluetooth.CHAR_WRITE_EVENT | Bluetooth.CHAR_READ_EVENT, handler=char1_cb_handler)

def char2_cb_handler(chr):
    events = chr.events()
    if  events & Bluetooth.CHAR_WRITE_EVENT:
        print("Write request on char2 with value = {}".format(chr.value()))
    else:
        print("Read request on char2 value = {}".format(chr.value()))

char2_cb = chr2.callback(trigger=Bluetooth.CHAR_WRITE_EVENT | Bluetooth.CHAR_READ_EVENT, handler=char2_cb_handler)
