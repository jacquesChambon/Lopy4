""" TOCS example usage """

import machine

dac = machine.DAC('P22')        # create a DAC object
adc = machine.ADC()             # create an ADC object
apin = adc.channel(pin='P13',attn=machine.ADC.ATTN_0DB)   # create an analog pin on P13

while True:
    print("DAC input : Please type a float value between 0 and 0.5 : ", end="")
    input_value=float(input())
    if input_value >=0.0 and input_value <=0.5:
        dac.write(input_value)
        print("ADC read value is %s mv" % apin.voltage())
