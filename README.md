# Perceptron Controller

Steps to setup the Controller


## Installation

STEP 1: update the raspberry pi files

```bash
  sudo apt update
  sudo apt upgrade
```

STEP 2: install the xbox controller driver 
```bash
sudo apt install xboxdrv
```

STEP 3:  disables the Enhanced Re-Transmission Mode (ERTM) of the Bluetooth module, with it, enabled the Xbox Controller won’t pair correctly.

```bash
echo 'options bluetooth disable_ertm=Y' | sudo tee -a /etc/modprobe.d/blutooth.conf
```

STEP 4: restart the raspberry pi 
```bash
sudo reboot
```

STEP 5: start bluetooth tools 
```bash
sudo bluetoothctl
```

STEP 6: within the bluetooth tools:

-> switch on agent 
```bash
agent on
```
-> select agent 
```bash
default-agent
```

STEP 7: scan for controller by running 
```bash
scan on
```

STEP 8: when the xontroller is visible on the command line note down the MAC address of the controller. It will look like: 
```bash
[NEW] Device B8:27:EB:A4:59:08 Wireless Controller
```

STEP 9: To connect with the controller type in the terminal 
```bash
connect CONTROLLER_MAC_ADDRESS
```
If th connection is successful you'll see this:
```bash
Attempting to connect to B8:27:EB:A4:59:08
[CHG] Device B8:27:EB:A4:59:08 Modalias: usb:v054Cp0268d0100
[CHG] Device B8:27:EB:A4:59:08 UUIDs:
        00001124-0000-1000-8000-00805f9b34fb
        00001200-0000-1000-8000-00805f9b34fb
```
STEP 10: add the controller to the trusted devices list
```bash
trust CONTROLLER_MAC_ADDRESS
```

STEP 11: Install toolset which allows us to check to see whether our Xbox One controller is working correctly.
```bash
sudo apt-get install joystick
```

STEP 12: Test the controller by running
```bash
sudo jstest /dev/input/js0
```
## Lidar wiring

## Lidar Wiring

- Red Wire --> 5V
- Black Wire --> GND
- White/Blue Wire --> Tx
- Green Wire --> Rx
Steps to setup serial port

STEP 1: go to raspberry pi settings

STEP 2: select interface option for raspberry pi

STEP 3: enable serial port 

STEP 4: install
```bash
python -m pip install pyserial
```
