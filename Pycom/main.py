# Pycom specific module & a few 'os micropython module' functions

import pycom
import os

pycom.nvs_set('temp', 25)
pycom.nvs_set('count', 10)

print("temp = %s, count = %s " % (pycom.nvs_get('temp'), pycom.nvs_get('count')))


pycom.nvs_erase('temp') # Erase the given key from the NVRAM memory area.
print("temp = %s, count = %s " % (pycom.nvs_get('temp'), pycom.nvs_get('count')))

pycom.nvs_erase_all() # Erase the entire NVRAM memory area.
print("temp = %s, count = %s " % (pycom.nvs_get('temp'), pycom.nvs_get('count')))

'''
pycom.wifi_on_boot([enable]) # Get or set the WiFi on boot flag.
pycom.wdt_on_boot([enable]) # Enables the WDT at boot time with the timeout in ms set by the function wdt_on_boot_timeout
pycom.wdt_on_boot_timeout([timeout]) # Sets or gets the WDT on boot timeout in milliseconds. The minimum value is 5000 ms.
'''

print("system info : %s, cwd : %s" % (os.uname() , os.getcwd()))
