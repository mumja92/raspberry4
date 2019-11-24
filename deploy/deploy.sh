#!/bin/bash
# Deploys image.rpi-sdimg to given device
# Usage: sudo deploy.sh <device> <image (optional)>
# ie sudo deploy.sh /dev/sdb
# todo: format device
echo "Please format and unmount device before start"

IMAGE_PATH="../raspberrypi4/tmp/deploy/images/raspberrypi4/mumja-image-raspberrypi4.rpi-sdimg"

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

if [ "$#" -lt 1 ]; then
    echo "Usage: sudo deploy.sh <device> <image (optional)>"
    exit 1
fi

DEVICE=$1
if [ ! -e "$DEVICE" ] || [[ ! $DEVICE == /dev/* ]]; then
    echo "Device $DEVICE does not exist"
    exit 1
fi

if [ ! -z "$2" ]; then
    IMAGE_PATH="$2"
fi

if [ ! -f "$IMAGE_PATH" ]; then
    echo "File: $IMAGE_PATH does not exist"
    exit 1
fi

SIZE_BYTES="$(blockdev --getsize64 $DEVICE)"


echo "Writing:"
echo "Device: $DEVICE"
echo -n "Device size: "
echo "$SIZE_BYTES" | numfmt --to=iec
echo "Image: $IMAGE_PATH"

read -p "Are you sure? [y]" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    dd if="$IMAGE_PATH" of="$DEVICE" bs=1M
else
    echo "aborted"
fi

