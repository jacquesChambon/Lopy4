""" TOCS example usage """

import pycom, time

print("Hello world")

def pled():
    pycom.heartbeat(False)
    pycom.rgbled(0xff00)
    time.sleep(5)
    pycom.heartbeat(True)
