BUILD="NT"



openwrt-ar71xx-generic-yun-16M-rootfs-squashfs-${BUILD}.bin: squashfs-root
	sh build.sh
	mksquashfs squashfs-root $@  -comp xz -all-root

squashfs-root: openwrt-ar71xx-generic-yun-16M-rootfs-squashfs.bin
	unsquashfs openwrt-ar71xx-generic-yun-16M-rootfs-squashfs.bin

clean:
	rm -rf squashfs-root	
