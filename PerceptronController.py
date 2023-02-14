#R2 trigger = acceleration
#L2 trigger = brakes
#right joystick = steering

import RPi.GPIO as GPIO
import time
import xbox

#This is not actual board pins. This is in BCM layout.
#Refer to BCM to BOARD layout over the internet to make actual connections
driverMotor = 23
breaksStepPin = 15
breaksDirectionPin = 40
steeringDirection = 15
steeringStepPin = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(driverMotor, GPIO.OUT) #driver motor
GPIO.setup(breaksStepPin, GPIO.OUT) #breaks step pin
GPIO.setup(breaksDirectionPin, GPIO.OUT) #breaks direction pin
GPIO.setup(steeringStepPin, GPIO.OUT) #steering step pin
GPIO.setup(steeringDirection, GPIO.OUT) #steering direction pin

ser = serial.Serial("/dev/ttyUSB0", 115200)

STEERING_MAX_ANGLE = 90
STEERING_MIN_ANGLE = -90
BREAKING_MAX_ANGLE = 0
BREAKING_STEP_SIZE = 30 #change accordingly
STEERING_MAX_POS = 0 #full coverage of 70 steps, angle of reference is
                     #same as the joystick value i.e. (-90 to 90)
    
applyBreaks = GPIO.LOW #change after checking stepper physicaly
releaseBreaks = GPIO.HIGH
steerLeft = GPIO.LOW #change after checking stepper physicaly 
steerRight = GPIO.HIGH

drivePower = GPIO.PWM(11,100)
drivePower.start(1) #starting the motor at one percent power

joy = xbox.Joystick()
r2TriggerValue = joy.rightTrigger() #value ranges from 0 to 1
l2TriggerValue = joy.leftTrigger() #value ranges from 0 to 1
steering = joy.rightX()

while not joy.Back(): #pressing the back key will stop the car 
    #Accelerate
    drivePower.changeDutyCycle(r2TriggerValue*100)
    data = ser.readline().strip()
    distance, strength = data.split(',')
    
    #Controller vibrate
    if distance < 100: # 100cm set as threshold distance
        vibrate()
    
    #Steer right
    if joy.rightX()>=STEERING_MAX_POS:
        steps = round(2.57*(joy.rightX() - STEERING_MAX_POS))
        steer(steps, steerRight, joy.rightX())
        STEERING_MAX_POS = pos
    
    #Steer left
    if joy.rightX()<STEERING_MAX_POS: 
        steps = round(abs(STEERING_MAx_POS - joy.rightX())*2.57)
        steer(steps, steerLeft, joy.rightX())
        STEERING_MAX_POS = pos
    
    #Apply breaks
    if l2TriggerValue>BREAKING_MAX_ANGLE:
        brake(l2TriggerValue, applyBrakes)
        BREAKING_MAX_ANGLE = l2TriggerValue
    
    #Release breaks
    if l2TriggerValue<BREAKING_MAX_ANGLE:
        brake(l2TriggerValue, releaseBrakes)
        BREAKING_MAX_ANGLE = l2TriggerValue
        
        
def brake(trigVal, direction):
    GPIO.output(breaksDirectionPin, direction)
        for i in range((trigVal-BREAKING_MAX_ANGLE)*BREAKING_STEP_SIZE):
            GPIO.output(breaksStepPin, GPIO.HIGH)
            time.sleep(0.010)
            GPIO.output(breaksStepPin, GPIO.LOW)
            time.sleep(0.010)
        
def steer(steps, direction, pos):
    GPIO.output(steeringDirection, direction)
    for i in range(steps):
        GPIO.output(steeringStepPin, GPIO.HIGH)
        time.sleep(0.010)
        GPIO.output(steeringStepPin, GPIO.LOW)
        time.sleep(0.010)
def vibrate():
    joy.set_rumble(1, 1, 0.5)
    time.sleep(1)
    joy.set_rumble(0, 0, 0)
    time.sleep(0.1)

drivePower.stop()
gpio.clean()
