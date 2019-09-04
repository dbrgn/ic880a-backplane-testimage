# iC880A Backplane Test Image

This is a build script for a Raspberry Pi 0 test image.

It is used to test the
[iC880A Backplane](https://github.com/dbrgn/ic880a-backplane/).

To build, type

    ./build.sh

Then copy the resulting image to an SD card with `dd`. The size of the image
should be around 130 MiB.

To copy it to the target SD:

    sudo dd if=buildroot-2019.02.4/output/images/sdcard.img of=/dev/YOURDEVICE bs=8M
    sync
