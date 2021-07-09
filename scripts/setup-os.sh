#!/bin/bash

# Update existing packages
sudo apt-get update
sudo apt-get upgrade --fix-missing
sudo apt autoremove

# Install required software
sudo apt-get install git python3-numpy python3-pip vim

# Change hostname
sudo sed --in-place --expression "s/raspberrypi/eink-radiator/" /etc/hostname /etc/hosts

sudo reboot
