# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal

from network import WLAN
import machine
wlan = WLAN(mode=WLAN.STA)

SSID=None
PASS=None

'''
SSID='iPhone 6S de Jacques'
PASS='0670726938'

SSID='Toscane'
PASS='0492420299'
'''

if not SSID:
    print('Type SSID : ', end='')
    SSID=input()
if not PASS:
    print('Type PASS : ', end='')
    PASS=input()

nets = wlan.scan()
for net in nets:
    if net.ssid == SSID:
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, PASS), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break
