#!/bin/bash
set -euo pipefail

VERSION="2018.02-rc1"
DIR="buildroot-$VERSION"
ARCHIVE="$DIR.tar.gz"
URL="https://buildroot.org/downloads/$ARCHIVE"
SHA1SUM=5f0f3100579e51793b2ce434f10c896f30b83a6b
WIFI_SSID="setme"
WIFI_PASS="setme"

echo -e "Building iC880A Backplane Test Image\n"

echo "==> Downloading buildroot"
if [ ! -f $ARCHIVE ]; then
    wget $URL
fi

echo "==> Verifying checksum"
if [ $SHA1SUM != $(sha1sum $ARCHIVE | cut -d' ' -f 1) ]; then
    echo "ERROR: Invalid checksum"
    exit 1
fi

echo "==> Unpacking buildroot"
tar xfz $ARCHIVE

echo "==> Copying config file"
cp buildroot-config $DIR/.config

echo "==> Copying board dir"
cp -R --preserve=mode ic880a-backplane $DIR/board/

echo "==> Patching config file"
sed -i "s/{{SSID}}/$WIFI_SSID/" $DIR/board/ic880a-backplane/post-build.sh
sed -i "s/{{PSK}}/$WIFI_PASS/" $DIR/board/ic880a-backplane/post-build.sh

echo "==> Build!"
cd $DIR
make all

echo "==> Done! Find the image at output/images/sdcard.img."
