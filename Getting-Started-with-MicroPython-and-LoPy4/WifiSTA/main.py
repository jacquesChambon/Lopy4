""" TOCS example usage """

import machine, os, pycom, time, socket, sys

rtc = machine.RTC()

print("Network config :", end='')
print(wlan.ifconfig())

print('Syncing time with "pool.ntp.org"')
rtc.ntp_sync("pool.ntp.org")
while not rtc.synced():
      time.sleep(0.05)
print("RTC NTP sync complete")
now = rtc.now()
print("Current Date and Time : %s/%s/%s at %s:%s" % (now[2], now[1], now[0], now[3], now[4]))

# A telnet like connection to emulate an HTTP GET request on google.com
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(4)

adr_info=socket.getaddrinfo('www.google.com', 80)
print("www.google.com addrinfo is : %s" % adr_info)
s.connect(adr_info[0][-1])

print("sending HTTP GET request")
s.send('GET\n')
print(s.recv(1000))
