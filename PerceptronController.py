import serial
import time
import RPi.GPIO as GPIO
import xbox


# LIDAR WIREING    
# Red Wire --> 5V
# Black Wire --> GND
# White/Blue Wire --> Tx
# Green Wire --> Rx
# 1. go to raspberry pi settings
# 2. select interface option for raspberry pi
# 3. enable serial port 
# 4. install (_>python -m pip install pyserial)

GPIO.setmode(GPIO.BCM)
steeringDirection = 15
steeringPulsePin = 24

ser = serial.Serial("/dev/ttyAMA0", 115200)

GPIO.setup(steeringDirection, GPIO.OUT)
GPIO.setup(steeringPulsePin, GPIO.OUT)

steerLeft = GPIO.LOW #change after checking stepper physicaly 
steerRight = GPIO.HIGH

STEERING_MAX_POS = 0 #full coverage of 70 steps, angle of reference is
                     #same as the joystick value i.e. (-90 to 90)

joy = xbox.Joystick()

while not joy.Back():
    data = ser.readline().strip()
    distance, strength = data.split(',')
    if distance < 100: # 100cm set as threshold distance
        vibrate()
    time.sleep(0.1)
    if joy.rightX()>=STEERING_MAX_POS:
        steps = round(2.57*(joy.rightX() - STEERING_MAX_POS))
        steer(steps, steerRight, joy.rightX())
        
    if joy.rightX()<STEERING_MAX_POS:
        steps = round(abs(STEERING_MAx_POS - joy.rightX())*2.57)
        steer(steps, steerLeft, joy.rightX())
        
GPIO.cleanup()

def steer(steps, direction, pos):
    GPIO.output(steeringDirection, direction)
    for i in range(steps):
        GPIO.output(steeringPulsePin, GPIO.HIGH)
        time.sleep(0.010)
        GPIO.output(steeringPulsePin, GPIO.LOW)
        time.sleep(0.010)
    STEERING_MAX_POS = pos
def vibrate():
    joy.set_rumble(1, 1, 0.5)
    time.sleep(1)
    joy.set_rumble(0, 0, 0)
