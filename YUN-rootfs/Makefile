BUILD="NT-1"
BASE_IMAGE= YunImage_v1.5.3.zip

.PHONY: files/image-info
packages= libpcap_1.1.1-2_ar71xx.ipk\
	tcpdump_4.2.1-3_ar71xx.ipk\
	avahi-autoipd_0.6.31-5_ar71xx.ipk\
	fping_2.4b2_to-ipv6-1_ar71xx.ipk

openwrt-ar71xx-generic-yun-16M-rootfs-squashfs-${BUILD}.bin: squashfs-root $(packages) files/image-info
	 $(foreach var,$(packages),./install_opkg.sh $(var) squashfs-root;)
	sh build.sh
	mksquashfs squashfs-root $@  -comp xz -all-root

openwrt-ar71xx-generic-yun-16M-rootfs-squashfs.bin: ${BASE_IMAGE}
	unzip $<

squashfs-root: openwrt-ar71xx-generic-yun-16M-rootfs-squashfs.bin
	unsquashfs openwrt-ar71xx-generic-yun-16M-rootfs-squashfs.bin

%.ipk:
	wget "http://downloads.arduino.cc/openwrtyun/1/packages/$@"

files/image-info:
	echo "ArduinoYun-Network-Tester YUN Image" > $@	
	echo "===================================" >> $@	
	echo "" >> $@
	echo "BaseImage: ${BASE_IMAGE}" >> $@
	echo "BUILD Version: ${BUILD}" >> $@
	echo "BUILD Date: `date -R`" >> $@
	echo "" >> $@
	echo "Pre-installed packages:" >> $@
	 $(foreach var,$(packages),echo " - $(var)" >> $@;)
	
		

clean:
	rm -rf squashfs-root
	rm -rf *.ipk
	rm -rf openwrt-ar71xx-generic-yun-16M-rootfs-squashfs-${BUILD}.bin
	rm -rf files/image-info
	rm -rf *.bin
