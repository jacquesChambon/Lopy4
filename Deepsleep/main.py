""" TOCS example usage """
import machine
from machine import Pin
import time

Wake_reason={0: 'None', machine.PWRON_WAKE: 'PWRON_WAKE', machine.PIN_WAKE: 'PIN_WAKE', machine.RTC_WAKE: 'RTC_WAKE', machine.ULP_WAKE: 'ULP_WAKE'}
print("Wake reason is: %s" % Wake_reason[machine.wake_reason()[0]])

def pin_handler(arg):
    time.sleep(0.5)
    print("Setting %s to listen for wakeup" % (arg.id()))
    machine.pin_deepsleep_wakeup([arg.id()],machine.WAKEUP_ALL_LOW, True)
    print("Going into deepsleep: %s" % (arg.id()))
    machine.deepsleep(20000)

p_in = Pin('P10', mode=Pin.IN, pull=Pin.PULL_UP)
p_in.callback(Pin.IRQ_FALLING, pin_handler)
