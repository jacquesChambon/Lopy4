LoRa
====

lora_receive.py is intended to be loaded on the receiver and lora_send.py on the sender.

On each device, you import the corresponding package.

Receiver
--------

`from lora_receive import *`

then you either run sync_rec() or async_rec(). 

They do the same job but the first one runs synchronously 
(ie waits for a message within a while True: loop) and the other one setup a callback 
that will be called whenever a message arrives. This one will return to the prompt (>>>) immediatly

if the input message is 6 hex digits, it will set the led color for 10s. 

Sender 
------

`import lora_send`

then you will be prompt for the message you want to transmit.

