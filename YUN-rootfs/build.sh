#!/bin/sh

basedir=squashfs-root/

for f in etc/arduino etc/ethers etc/uci-defaults etc/uhttpd.crt etc/uhttpd.key usr/lib/opkg/info
do                                                                              
echo rm -rf $basedir$f                                                              
done     
for f in arduino firewall wireless dhcp network_dist ucitrack luci uhttpd  
do
rm -rf ${basedir}etc/config/$f
done

cp files/network ${basedir}etc/config/network
cp files/boot ${basedir}etc/init.d/boot
cp files/done ${basedir}etc/init.d/done
cp files/rc.local ${basedir}etc/rc.local
for service in cron luci_fixtime handle_wifi_reset rename-wifi-if-access-point firewall usb generate_new_gpg_key uhttpd luci_dhcp_migrate dnsmasq avahi-daemon sysntpd rngd rngd-turn-off delete_uhttpd_cert triggerhappy defconfig dbus
do
rm -f ${basedir}etc/rc.d/*$service
done

for m in 01-crypto-core 02-crypto-hash 03-crypto-manager 09-crypto-aes 09-crypto-arc4 20-cfg80211 21-mac80211 27-ath9k-common 28-ath9k 30-fs-ntfs 30-ppp 40-scsi-core 41-ipt-conntrack 40-ipt-core 42-ipt-nat 45-ipt-nathelper 60-video-core 30-fs-reiserfs 41-pppoe 40-pppox 30-gpio-button-hotplug 30-fs-hfs 30-fs-hfsplus  20-lib-crc-ccitt 30-fs-ext4 50-ledtrig-default-on 50-ledtrig-netdev 50-ledtrig-timer 60-leds-gpio 80-fuse 51-i2c-core 20-lib-crc16
do
rm -f ${basedir}etc/modules.d/$m
done

for m in 30-fs-reiserfs  02-crypto-hash 01-crypto-core 30-fs-ext4 20-lib-crc16
do
rm -f ${basedir}etc/modules-boot.d/$m
done

echo extroot_settle_time=\"0\" > ${basedir}lib/preinit/00_extroot.conf
