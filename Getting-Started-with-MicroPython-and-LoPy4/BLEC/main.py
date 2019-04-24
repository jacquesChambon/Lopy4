from network import Bluetooth
import time
bt = Bluetooth()
bt.start_scan(-1)

def char_cb(char):
  print('char {} value modified = {}'.format(hex(char.uuid()), char.read()))

def bt_cb(bt):
    print("bt disconnected")

while True:
  print("loop")
  adv = bt.get_adv()
  if adv and bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL) == 'test':
      try:
          bt.stop_scan()
          conn = bt.connect(adv.mac)
          print("connected to My iPhone")
          bt.callback(Bluetooth.CLIENT_DISCONNECTED, bt_cb)
          services = conn.services()
          for service in services:
              print('service UUID = {}'.format(service.uuid() if isinstance(service.uuid(),bytes) else hex(service.uuid())))
              if service.uuid() == 0x1111:
                 chars = service.characteristics()
                 for char in chars:
                     time.sleep(0.050)
                     char.callback(trigger=Bluetooth.CHAR_NOTIFY_EVENT, handler=char_cb)
                     print('char {} value = {}'.format(hex(char.uuid()), char.read()))
          break
      except:
          print("erreur")
          raise
  else:
      time.sleep(0.050)
