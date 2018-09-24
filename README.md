# ArduinoYun-Network-Tester
Simple battery-powered Netowork tester built on ArduinoYun and Python

## About the custom roofs
**You don't have to flash your YUN with a new rootfs to make the Network-Tester scripts work!!**

The main reason for a custom rootfs is to speed up the boot-process by removing the 20s wait for external usb devices. This can imho only be changed in the sqashfs, because the script is executed before the overlay-fs is loaded.


