#!/bin/bash

# This is meant to be run on the laptop just after the SD card has been imaged by Etcher

WIRELESS_SSID=$(jq -r '.["wifi-ssid"]' ../secrets/pipeline-creds.json)
WIRELESS_PASSWORD=$(jq -r '.["wifi-password"]' ../secrets/pipeline-creds.json)

if ! ls /Volumes/boot/ ; then
    echo Check that the SD card is mounted?
    exit 1
fi

# Create touchfile to enable ssh by default
touch /Volumes/boot/ssh

# Initialize the WiFi settings
echo "country=us
update_config=1
ctrl_interface=/var/run/wpa_supplicant
network={
 scan_ssid=1
 ssid=\"${WIRELESS_SSID}\"
 psk=\"${WIRELESS_PASSWORD}\"
}" > /Volumes/boot/wpa_supplicant.conf

# TODO: exit config.txt and uncomment dtparam=spi=on

echo "Done!"
