#!/bin/bash
set -e

BOARD_DIR="$(dirname $0)"
BOARD_NAME="$(basename ${BOARD_DIR})"
RPI_BOARD_DIR="$(dirname $0)/../raspberrypi"
RPI_BOARD_NAME="raspberrypi0"
GENIMAGE_CFG="${RPI_BOARD_DIR}/genimage-${RPI_BOARD_NAME}.cfg"
GENIMAGE_TMP="${BUILD_DIR}/genimage.tmp"

echo "Copying config.txt"
cp "$BOARD_DIR/config.txt" "$BINARIES_DIR/rpi-firmware/config.txt"

rm -rf "${GENIMAGE_TMP}"

genimage                           \
	--rootpath "${TARGET_DIR}"     \
	--tmppath "${GENIMAGE_TMP}"    \
	--inputpath "${BINARIES_DIR}"  \
	--outputpath "${BINARIES_DIR}" \
	--config "${GENIMAGE_CFG}"

exit $?
