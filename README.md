# ArduinoYun-Network-Tester
Simple battery-powered Netowork tester built on ArduinoYun and Python

## The idea..
..is to build a handheld Network Tester that can run complex tests while givin a simple God/Bad indicator. The NetworkTester provides 5 two-colored LEDs to display the test-results. The tests themselfs are written in python and run on the linux part of the ArduinoYun.

The current tests feature Dante Clock(PTP IEEE 1588), Dante Hello, Lake Controller Hello and sACN. Those protocolls are common in professional audio and lighting networks.

## Installation
1. Build the LED-Display(schematics in *Electronics/Arduino-LED/*) or any kind of display you like.
2. Upload the *Ardunio-LED* sketch to the ardunio on your Yun. Adapt it to match your display of course.
3. (optional) build and load the custom rootfs to your YUN(see *YUN-rootfs/* for details)
4. copy the *src/* folder to the Linux on your YUN and run the install script from inside the *src/* folder 


## About the custom roofs
**You don't have to flash your YUN with a new rootfs to make the Network-Tester scripts work!!**

The main reason for a custom rootfs is to speed up the boot-process by removing the 20s wait for external usb devices. This can imho only be changed in the sqashfs, because the script is executed before the overlay-fs is loaded.

