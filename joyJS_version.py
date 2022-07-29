# ESP32-S2 wifi radio SoftAP changes:
#
# the key concept is `mode`, one of: Station (STA), Access Point (AP), STA+AP, (NONE)
# before now, ESP32-S2 wifi was always in Station mode, ready to scan or connect to an AP
# now Station and AP can be independently controlled, and the ESP32-S2 can be either, both, or neither
# note that AP mode isn't a router; it's typically going to be an IP server endpoint to IP clients
#
# mode is also independent of `enabled` state, which turns wifi on or off
# mode can be changed when wifi is enabled or not enabled
#
# the maximum number of connected stations is currently 4

def web_page():
  return open('index.html', 'r').read()




#import urllib.parse
import wifi
import ipaddress
import socketpool
import time

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
PORT = 80
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
while True:
  try:
    print("Accepting connections")
    conn, addr = s.accept()
    conn.settimeout(TIMEOUT)
    print("Accepted from", addr)

    size = conn.recv_into(inbuf, MAXBUF)
    print("Received", size, "bytes")
    print(inbuf[:size])
    first_line=inbuf[:size].decode().split('\r\n')[0]
    url=first_line.split(' ')[1]
    print("URL:", url)
    scheme, netloc, path, params, qs, fragment = circuitpython_parse.urlparse(url)
    qs = circuitpython_parse.parse_qs(qs)
    path=path.toLowerCase()
    
    if(path=="/"):

      if(qs and "test" in qs.keys()):
        test = qs["test"]
        print(test)
        print(test[0])

        outbuf=b"HTTP/1.0 200 OK\r\n" + \
          b"Connection: close\r\n" + \
          b"\r\n" + \
          b"<html>"+ web_page() + \
          b"<hr style=\"margin: " +  bytes(str(50 * int(test[0])),'utf8') + b"px ;background-color:rgba(0,0," +  bytes(str(255 * int(test[0])),'utf8') + b",1);\"><pre>" + \
          inbuf[:size] + \
          b"</pre></html>"
      else:
          outbuf = b"HTTP/1.0 200 OK\r\n" + \
          b"Connection: close\r\n" + \
          b"\r\n" + \
          b"<html>"+ web_page() + \
          b"<hr><pre>" + \
          inbuf[:size] + \
          b"</pre></html>"

    elif(path=="/joy.js"):
       open('joy.js','rb').readinto(outbuf)
       outbuf = b"HTTP/1.0 200 OK\r\n" + \
              b"Connection: close\r\n" + \
              b"\r\n" + \
              outbuf

    else:
        outbuf = b"HTTP/1.0 404 Not Found\r\n" + \
          b"Connection: close\r\n" + \
          b"\r\n"

    conn.send(outbuf)
    print("Sent", outbuf.decode())
    print("Sent", len(outbuf), "bytes")

    conn.close()
  except:
    conn.close()

# the rest is exercise left for the reader, could try some socket stuff
# (some examples at <https://github.com/anecdata/Socket>)
# or anything else that's convenient to set up.

print("Stopping the AP...")
wifi.radio.stop_ap()  # close down the shop
# </fin>