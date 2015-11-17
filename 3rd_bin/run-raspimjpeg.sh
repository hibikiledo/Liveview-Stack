#!/bin/bash

mkdir -p /var/www/media
mkdir -p /dev/shm/mjpeg
mknod /var/www/FIFO p
chmod 666 /var/www/FIFO

screen -S raspimjpeg ./raspimjpeg --config raspimjpeg.config

