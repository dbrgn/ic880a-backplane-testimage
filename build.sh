#!/bin/bash
set -euo pipefail

VERSION="2019.02.4"
DIR="buildroot-$VERSION"
ARCHIVE="$DIR.tar.gz"
URL="https://buildroot.org/downloads/$ARCHIVE"
SHA1SUM=b7f3a717742e06ed6cb309e8e3d6925de1164808
WIFI_SSID="setme"
WIFI_PASS="setme"

echo -e "Building iC880A Backplane Test Image\n"

echo "==> Downloading buildroot"
if [ ! -f $ARCHIVE ]; then
    wget $URL
fi

echo "==> Verifying checksum"
if [ $SHA1SUM != "$(sha1sum $ARCHIVE | cut -d' ' -f 1)" ]; then
    echo "ERROR: Invalid checksum"
    exit 1
fi

echo "==> Unpacking buildroot"
tar xfz $ARCHIVE

echo "==> Apply config"
rm -f $DIR/.config
cp buildroot-defconfig $DIR/configs/ic880a_backplane_defconfig
cd $DIR
cat configs/raspberrypi0w_defconfig configs/ic880a_backplane_defconfig > configs/merged_defconfig
make merged_defconfig
cd ..

echo "==> Copying board dir"
cp -R --preserve=mode ic880a-backplane $DIR/board/

echo "==> Patching config file"
sed -i "s/{{SSID}}/$WIFI_SSID/" $DIR/board/ic880a-backplane/post-build.sh
sed -i "s/{{PSK}}/$WIFI_PASS/" $DIR/board/ic880a-backplane/post-build.sh

echo "==> Build!"
cd $DIR
make all

echo "==> Done! Find the image at output/images/sdcard.img."
