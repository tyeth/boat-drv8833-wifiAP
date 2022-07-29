# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import pwmio
import board
import busio
import neopixel
import time
import adafruit_motor.motor as motor


pwm_a1 = pwmio.PWMOut(board.MOSI, frequency=1)
pwm_a2 = pwmio.PWMOut(board.MISO, frequency=1)
pwm_b1 = pwmio.PWMOut(board.SCK, frequency=1)
pwm_b2 = pwmio.PWMOut(board.RX, frequency=1)

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
    return ("200 OK", [], "engineAdjusted!" + along + "," + up)



def move_motors(left_motor, right_motor):
    print("left_motor: ", left_motor)
    print("right_motor: ", right_motor)
    m1.throttle=left_motor
    m2.throttle=right_motor

print("starting motor test")
i=1
while(True):
    if( i==10):
        i=0
    else:
        i+=1
    m2.throttle=1
    time.sleep(2)
    m2.throttle=0
    time.sleep(2)
    m2.throttle=-1
    time.sleep(2)
    print("looping #",i)

    # print(adjustMotors(0,0))
    # time.sleep(1)
    # print(adjustMotors(0,100))
    # time.sleep(1)
    # print(adjustMotors(0,0))
    # time.sleep(1)
    # print(adjustMotors(0,-100))
    # time.sleep(1)
    
