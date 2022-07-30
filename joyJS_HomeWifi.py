# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import pwmio
import board
import busio
from digitalio import DigitalInOut
import neopixel

import adafruit_motor.motor as motor


import wifi
import wsgiserver as server
#from adafruit_esp32spi import adafruit_esp32spi
# import adafruit_esp32spi.adafruit_esp32spi_wifimanager as wifimanager
# import adafruit_esp32spi.adafruit_esp32spi_wsgiserver as server
from adafruit_wsgi.wsgi_app import WSGIApp , Request

secrets={}
secrets["ssid"]="free4all_2G"
secrets["password"]="password"

# Get wifi details and more from a secrets.py file
# try:
#     from secrets import secrets
# except ImportError:
#     print("WiFi secrets are kept in secrets.py, please add them there!")
#     raise

pwm_a1 = pwmio.PWMOut(board.MOSI, frequency=50)
pwm_a2 = pwmio.PWMOut(board.MISO, frequency=50)
pwm_b1 = pwmio.PWMOut(board.SCK, frequency=50)
pwm_b2 = pwmio.PWMOut(board.RX, frequency=50)

m1 = motor.DCMotor(pwm_a1, pwm_a2)
m2 = motor.DCMotor(pwm_b1, pwm_b2)

def adjustMotors(along,up):
    print("x: ",along,"y: ",up)
    left_right = int(along)
    front_back = int(up)
    
    print(front_back+left_right)
    print(front_back-left_right)
    left_motor = front_back + left_right
    right_motor = front_back - left_right
    
    # Scale factor defaults to 1
    scale_factor = 1.0
    
    # Calculate scale factor
    if abs(left_motor) > 100 or abs(right_motor) > 100:
        # Find highest of the 2 values, since both could be above 100
        print(abs(left_motor),abs(right_motor))
        x = max(abs(left_motor), abs(right_motor))
    
        # Calculate scale factor
        scale_factor = 100.0 / x
    
    print("scale",scale_factor)

    # Use scale factor, and turn values back into integers
    left_motor = float( int(left_motor * scale_factor) /100.0)
    right_motor = float( int(right_motor * scale_factor) /100.0)
    
    # Actually move the motors
    move_motors(left_motor, right_motor)
    print("engineAdjust!",along,up)
    return ("200 OK", [], "engineAdjusted!" + along + "," + up + "\r\nleft:" + str(left_motor) + " right:" + str(right_motor))



def move_motors(left_motor, right_motor):
    print("left_motor: ", left_motor)
    print("right_motor: ", right_motor)
    m1.throttle=left_motor
    m2.throttle=right_motor

# This example depends on a WSGI Server to run.
# We are using the wsgi server made for the ESP32

print("ESP32 SPI simple web app test!")


# If you are using a board with pre-defined ESP32 Pins:
# esp32_cs = DigitalInOut(board.ESP_CS)
# esp32_ready = DigitalInOut(board.ESP_BUSY)
# esp32_reset = DigitalInOut(board.ESP_RESET)

# If you have an externally connected ESP32:
# esp32_cs = DigitalInOut(board.D9)
# esp32_ready = DigitalInOut(board.D10)
# esp32_reset = DigitalInOut(board.D5)

# spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
# esp = adafruit_esp32spi.ESP_SPIcontrol(
#     spi, esp32_cs, esp32_ready, esp32_reset
# )  # pylint: disable=line-too-long

"""Use below for Most Boards"""
status_light = neopixel.NeoPixel(
    board.NEOPIXEL, 1, brightness=0.2
)  # Uncomment for Most Boards
"""Uncomment below for ItsyBitsy M4"""
# import adafruit_dotstar as dotstar
# status_light = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=1)

## If you want to connect to wifi with secrets:
#wifi = wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light, debug=True)
#wifi.radio.connect(secrets["ssid"], secrets["password"])

## If you want to create a WIFI hotspot to connect to with secrets:
secrets = {"ssid": "CircuitPython-AP", "password": "password"}
# wifi = wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)
# wifi.create_ap()

## To you want to create an un-protected WIFI hotspot to connect to with secrets:"
# secrets = {"ssid": "My ESP32 AP!"}
# wifi = wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)
# wifi.create_ap()

# Here we create our application, registering the
# following functions to be called on specific HTTP GET requests routes

web_app = WSGIApp()


@web_app.route("/led_on/<r>/<g>/<b>/<w>")
def led_on(request, r, g, b, w):  # pylint: disable=unused-argument
    print("led on!")
    status_light.fill((int(r), int(g), int(b),1))
    return ("200 OK", [], "led on!")


@web_app.route("/led_off")
def led_off(request):  # pylint: disable=unused-argument
    print("led off!")
    status_light.fill(0)
    return ("200 OK", [], "led off!")

@web_app.route("/coords/<x>/<y>")
def engineAdjust(request,x,y):
    return adjustMotors(x,y)
    

@web_app.route("/", methods=["GET"])
def index(request):
    return ("200 OK", [], open("index.html", "r").read())

@web_app.route("/joy.js", methods=["GET"])
def index(request):
    return ("200 OK", [], open("joy.js", "r").read())


# Here we setup our server, passing in our web_app as the application
#server.set_interface(esp)
#wsgiServer = server.WSGIServer(80, application=web_app)

#server.set_interface(wifi.radio)
HOST = repr(wifi.radio.ipv4_address)
PORT = 80  # Port to listen on
wsgiServer = server.WSGIServer(PORT, application=web_app)
print(HOST, PORT)
print("open this IP in your browser: ", wsgiServer.pretty_ip())

# print(esp.get_time())
# Start the server

wsgiServer.start()
while True:
    # Our main loop where we have the server poll for incoming requests
    #try:
        wsgiServer.update_poll()
        # Could do any other background tasks here, like reading sensors
    # except (ValueError, RuntimeError) as e:
    #     print("Failed to update server, restarting ESP32\n", e)
    #     wifi.reset()
    #     continue

