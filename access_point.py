# Webserver to send RGB data
# Tony Goodhew 5 July 2022
import network
import socket
import time
from machine import Pin, ADC
from shared import SSID, PASSWORD

wlan: network.WLAN = network.WLAN(network.AP_IF)
wlan.config(ssid=SSID, key=PASSWORD, pm=wlan.PM_NONE)
wlan.active(True)

# Wait for connect or fail
max_wait: int = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError(wlan.status())
else:
    print('connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])

# Open socket
addr = socket.getaddrinfo('192.168.4.1', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print(request)
        # Do not unpack request
        # We reply to any request the same way
        # Generate 3 values to send back

        cl.send("test")
        print("Sent:")
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')
