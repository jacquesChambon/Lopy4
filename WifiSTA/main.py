""" TOCS example usage """

from machine import SD, RTC
import os
import pycom
import time

rtc = RTC()

'''
sd = SD()

os.mount(sd, '/sd')
print("SD card files :")
print(os.listdir('/sd'))
'''

print("Network config :")
print(wlan.ifconfig())

def pled():
    pycom.heartbeat(False)
    pycom.rgbled(0xff00)

print('Syncing time with "pool.ntp.org"')
rtc.ntp_sync("pool.ntp.org")
while not rtc.synced():
      time.sleep(0.05)
print("RTC NTP sync complete")
now = rtc.now()
print("Current Date and Time : %s/%s/%s at %s:%s" % (now[2], now[1], now[0], now[3], now[4]))
