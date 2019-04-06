""" TOCS example usage """
from myAlarm import Clock
from machine import Pin

p_led=Pin('P9',mode=Pin.OUT)
p_button=Pin('P10',mode=Pin.IN,pull=Pin.PULL_UP)

def p_button_handler(pin):
    print('Pin Interrupt on %s ' % pin)
    p_led(0)

p_button.callback(Pin.IRQ_FALLING, p_button_handler)

clock=Clock(p_led,period=5,max_count=10)
