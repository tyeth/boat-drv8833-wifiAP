


CONTENT = b"""\
HTTP/1.0 200 OK

Hello #%d from MicroPython!
"""


import wifi
import socketpool
import ipaddress
import time
import ssl as ssl

import circuitpython_parse

#from secrets import secrets

# at this point, the ESP32-S2 is running as a station (init default), and if desired can connect to any AP

# the following two lines are not new APIs, but they are useful to test in combination with mode changes:
wifi.radio.enabled = False  # turns wifi off, mode is retained or can be changed while not enabled
wifi.radio.enabled = True  # turns wifi back on
print("Wi-Fi Enabled?", wifi.radio.enabled)

print(dir(wifi.radio))  # useful reference

print("Stopping the (default) station...")
wifi.radio.stop_station()  # now the device is in NONE mode, neither Station nor Access Point
# print("(Re-)Starting the station...")
# wifi.radio.start_station()  # would restart the station and later you would have both Station and AP running

# start the AP, `channel` of your choosing, `authmode` of your choosing:
# The Access Point IP address will be 192.168.4.1
# ...if that collides with your LAN, you may need to isolate the external station from your LAN
print("Starting AP...")
ssid = 'CircuitPython-AP'
password = 'password'
wifi.radio.start_ap(ssid=ssid, password=password, channel = 13, max_connections = 4)#,authmode=WPA2)

# connect from some client(s), check their interfaces to verify the wi-fi is connected, channel, authmode,...


# Fudge an HTTP response back to a browser on a connected wifi station
HOST = ""  # see below
PORT = 8443
TIMEOUT = None
BACKLOG = 2
MAXBUF = 1024

# get some sockets
pool = socketpool.SocketPool(wifi.radio)

print("AP IP Address:", wifi.radio.ipv4_address_ap)
print("      Gateway:", wifi.radio.ipv4_gateway_ap)
print("       Subnet:", wifi.radio.ipv4_subnet_ap)
HOST = str(wifi.radio.ipv4_address_ap)

print("Create TCP Server socket", (HOST, PORT))
s = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
s.settimeout(TIMEOUT)

s.bind((HOST, PORT))
s.listen(BACKLOG)
print("Listening")

inbuf = bytearray(MAXBUF)
counter=0
while True:
    print("Accepting connections")
    conn, addr = s.accept()
   
    client_s = conn
    client_addr = addr
    print("Client address:", client_addr)
    print("Client socket:", client_s)
    ssl_context = ssl.create_default_context() # purpose=ssl.Purpose.SERVER_AUTH) # .SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.check_hostname = False
    #ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    client_s = ssl_context.wrap_socket(client_s, server_side=True)
    
    print(client_s)
    print("Request:")
    if True: #use_stream:
        # Both CPython and MicroPython SSLSocket objects support read() and
        # write() methods.
        # Browsers are prone to terminate SSL connection abruptly if they
        # see unknown certificate, etc. We must continue in such case -
        # next request they issue will likely be more well-behaving and
        # will succeed.
        try:
            req = client_s.read(4096)
            print(req)
            if req:
                client_s.write(CONTENT % counter)
        except Exception as e:
            print("Exception serving request:", e)
    else:
        print(client_s.recv(4096))
        client_s.send(CONTENT % counter)
    client_s.close()
    counter += 1
    print()


# the rest is exercise left for the reader, could try some socket stuff
# (some examples at <https://github.com/anecdata/Socket>)
# or anything else that's convenient to set up.

print("Stopping the AP...")
wifi.radio.stop_ap()  # close down the shop
# </fin>

