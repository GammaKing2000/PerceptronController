#STEP 1: update the raspberry pi files (_>sudo apt update and sudo apt upgrade)
#STEP 2: install the xbox controller driver (_>sudo apt install xboxdrv)
#STEP 3:  disables the Enhanced Re-Transmission Mode (ERTM) of the 
#         Bluetooth module, with it, enabled the Xbox Controller won’t 
#         pair correctly.
#      _>echo 'options bluetooth disable_ertm=Y' | sudo tee -a /etc/modprobe.d/blutooth.conf
#STEP 4: restart the raspberry pi (_>sudo reboot)
#STEP 5: start bluetooth tools (_>sudo bluetoothctl)
#STEP 6: within the bluetooth tools:
#       -> switch on agent (_>agent on)
#       -> select agent (_>default-agent)
#STEP 7: scan for controller by running (_>scan on)
#STEP 8: when the xontroller is visible on the command line note down the
#        MAC address of the controller.
#It will look like ([NEW] Device B8:27:EB:A4:59:08 Wireless Controller)
#STEP 9: To connect with the controller type in the terminal (_>connect CONTROLLER_MAC_ADDRESS)
# If th connection is successful you'll see this:
# _>Attempting to connect to B8:27:EB:A4:59:08
# _>[CHG] Device B8:27:EB:A4:59:08 Modalias: usb:v054Cp0268d0100
# _>[CHG] Device B8:27:EB:A4:59:08 UUIDs:
# _>        00001124-0000-1000-8000-00805f9b34fb
# _>        00001200-0000-1000-8000-00805f9b34fb
#STEP 10: add the controller to the trusted devices list (_>trust CONTROLLER_MAC_ADDRESS)
#STEP 11: Install toolset which allows us to check to see whether our
#         Xbox One controller is working correctly.
#         (_>sudo apt-get install joystick)
#STEP 12: Test the controller by running (_>sudo jstest /dev/input/js0)

#R2 trigger = acceleration
#L2 trigger = brakes
#right joystick = steering

# https://www.youtube.com/watch?v=YEYBbFdus-Q 

import RPi.GPIO as gpio
import time
import xbox

driverMotor = 11
breaksStepPin = 22
breaksDirectionPin = 21
steeringStepPin = 25
steeringDirectionPin = 8

gpio.setmode(gpio.BOARD)
gpio.setup(driverMotor, gpio.OUT) #driver motor
gpio.setup(breaksStepPin, gpio.OUT) #breaks step pin
gpio.setup(breaksDirectionPin, gpio.OUT) #breaks direction pin
gpio.setup(steeringStepPin, gpio.OUT) #steering step pin
gpio.setup(steeringDirectionPin, gpio.OUT) #steering direction pin

STEERING_MAX_ANGLE = 90
STEERING_MIN_ANGLE = -90
BREAKING_MAX_ANGLE = 0
BREAKING_STEP_SIZE = 30 #change accordingly
applyBreaks = gpio.LOW
releaseBreaks = gpio.HIGH

drivePower = gpio.PWM(11,100)

drivePower.start(1) #starting the motor at one percent power

joy = xbox.Joystick()
r2TriggerValue = joy.rightTrigger() #value ranges from 0 to 1
l2TriggerValue = joy.leftTrigger() #value ranges from 0 to 1
steering = joy.rightX() 

while not joy.Back(): #pressing the back key will stop the car 
    drivePower.changeDutyCycle(r2TriggerValue*100)
    if l2TriggerValue>BREAKING_MAX_ANGLE:
        gpio.output(breaksDirectionPin, applyBreaks)
        for i in range((l2TriggerValue-BREAKING_MAX_ANGLE)*BREAKING_STEP_SIZE):
            gpio.output(breaksStepPin, gpio.HIGH)
            time.sleep(0.010)
            gpio.output(breaksStepPin, gpio.LOW)
            time.sleep(0.010)
        BREAKING_MAX_ANGLE = l2TriggerValue
    elif l2TriggerValue<BREAKING_MAX_ANGLE:
        gpio.output(breaksDirectionPin, releaseBreaks)
        for i in range((BREAKING_MAX_ANGLE-l2TriggerValue)*BREAKING_STEP_SIZE):
            gpio.output(breaksStepPin, gpio.HIGH)
            time.sleep(0.010)
            gpio.output(breaksStepPin, gpio.LOW)
            time.sleep(0.010)
        BREAKING_MAX_ANGLE = l2TriggerValue


    



drivePower.stop()
gpio.clean()