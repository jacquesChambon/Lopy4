# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal

from network import WLAN
import machine
wlan = WLAN(mode=WLAN.STA)

nets = wlan.scan()
for net in nets:
    if net.ssid == 'iPhone 6S de Jacques':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, '0670726938'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break
