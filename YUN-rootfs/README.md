# ArduinoYun-Network-Tester YUN Image
## Why flash a custom rootfs?
**You don't have to flash your YUN with a new rootfs to make the Network-Tester scripts work!!**

The main reason for a custom rootfs is to speed up the boot-process by removing the 20s wait for external usb devices. This can imho only be changed in the sqashfs, because the script is executed before the overlay-fs is loaded.

## What else is different in the new rootfs?

The script radically removes some things I think are not needed on a Network-Tester. 

* Default Network settings: Wifi disabled, LAN 99.99.99.99/24, gw: 99.99.99.98
* Removed system services from init files: wifi-live-or-reset, syslogd
* set extroot_settle_time to zero in /lib/preinit/00_extroot.conf
* removes many modules from startup
* removes many services from startup
* removes some files and folders

You might want to checkout the build.sh script for more details.



## How to build build the rootfs
The script doesn't build a new rootfs. It just changes some files in the image provided by arduino.

1. Download the Image
Get the image from the website below and unpack all files into this diretory
https://www.arduino.cc/en/Tutorial/YunUBootReflash

2. Install mksquashfs

3. Build your own rootfs
just type `make` 

4. Upload the rootfs to your YUN
Just follow the steps in the official manual but without the step "Reflashing U-Boot". Make sure you change the name of the rootf-image accordingly.
https://www.arduino.cc/en/Tutorial/YunUBootReflash

