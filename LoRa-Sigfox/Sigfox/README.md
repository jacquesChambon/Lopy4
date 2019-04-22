Sigfox
======

the `sigfox_rest_server.py` is intended to run on a server accessible from the Internet. 
It will be called by Sigfox Cloud to handle messages coming from teh sigfox devices

`sigfox_send.py` must be loaded on the device.

`from sigfox_send import *`

to send a message: `send('azerty')`

to send and wait for a response: `send_and_receive('azerty')`

there is a 60 seconds timeout on the socket. It will raise an error if
the response does not come in this timeframe.