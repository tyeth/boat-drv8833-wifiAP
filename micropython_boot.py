# Complete project details at https://RandomNerdTutorials.com

try:
  import usocket as socket
except:
  import socket

import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'MicroPython-AP'
password = '123456789'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)

while ap.active() == False:
  pass

print('Connection successful')
print(ap.ifconfig())

def web_page():
  html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
  <body><h1>Hello boat captain!</h1>
  </body></html>"""

  html = """
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Accelerometer Demo</title>

            <style>
            .indicatorDot{
                width: 30px;
                height: 30px;
                background-color: #ffab56;
                border-radius: 50%;
                position:fixed;
            }
            </style>

        <script></script>
        </head>
        <body style="background-color:lightblue;">
            <button id="accelPermsButton"  style="height:50px;" onclick="getAccel()"><h1>Get Accelerometer Permissions</h1></button>
            <div class="indicatorDot" style="left:30%; top:30%;"></div>
        </body>
        <script>
        var px = 50; // Position x and y
        var py = 50;
        var vx = 0.0; // Velocity x and y
        var vy = 0.0;
        var updateRate = 1/60; // Sensor refresh rate

        function getAccel(){
            DeviceMotionEvent.requestPermission().then(response => {
                if (response == 'granted') {
            // Add a listener to get smartphone orientation 
                // in the alpha-beta-gamma axes (units in degrees)
                    window.addEventListener('deviceorientation',(event) => {
                        // Expose each orientation angle in a more readable way
                        rotation_degrees = event.alpha;
                        frontToBack_degrees = event.beta;
                        leftToRight_degrees = event.gamma;
                        
                        // Update velocity according to how tilted the phone is
                        // Since phones are narrower than they are long, double the increase to the x velocity
                        vx = vx + leftToRight_degrees * updateRate*2; 
                        vy = vy + frontToBack_degrees * updateRate;
                        
                        // Update position and clip it to bounds
                        px = px + vx*.5;
                        if (px > 98 || px < 0){ 
                            px = Math.max(0, Math.min(98, px)) // Clip px between 0-98
                            vx = 0;
                        }

                        py = py + vy*.5;
                        if (py > 98 || py < 0){
                            py = Math.max(0, Math.min(98, py)) // Clip py between 0-98
                            vy = 0;
                        }
                        
                        dot = document.getElementsByClassName("indicatorDot")[0]
                        dot.setAttribute('style', "left:" + (px) + "%;" +
                                                    "top:" + (py) + "%;");
                        
                    });
                }
            });
        }
        </script>
    </html>
"""

  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  print('Content = %s' % str(request))
  response = web_page()
  conn.send(response)
  conn.close()