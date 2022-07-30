# Dual engine Boat controlled by Wifi access point running on Adafruit QTPY ESP32-S2 and DRV8833 motor controller

Creates access point running under "CircuitPython-AP", "password" and webpage under [http://192.168.4.1/](http://192.168.4.1/)

You can fire test values using http://192.168.4.1/coords/0/0 (0's can be +/-100) or just use the joystick on the main page.
There is an interface to the LED/Neopixel [http://192.168.4.1/led_on/&lt;r>/&lt;g>/&lt;b>/&lt;w>](http://192.168.4.1/led_on/15/10/20/1) (w is ignored but must be supplied, all values 0-255)

## See fritzing circuit
![fritzing circuit preview](https://raw.githubusercontent.com/tyeth/boat-drv8833-wifiAP/master/Circuit.png)


# Free SSL Certificate for 192.168.4.1 for CircuitPython MicroPython fun and games.
### 192dot168dot4dot1.gundryconsultancy.com resolves to 192.168.4.1
## I'll try to keep the repository updated, but failing that I've linked to the regularly updated certificate files from my server. 



## The certificates are valid for 90days from issue (whenever that is - first issued 2022-07-24).


[SSL.CA](https://www.gundryconsultancy.com/ssl.ca)

[SSL.cert](https://www.gundryconsultancy.com/ssl.cert)

[SSL.key](https://www.gundryconsultancy.com/ssl.key)

[SSL.combined](https://www.gundryconsultancy.com/ssl.combined)

[SSL.everything](https://www.gundryconsultancy.com/ssl.everything)


You'll want to run tinydns or some other dns service on the microcontroller / wifi access point.