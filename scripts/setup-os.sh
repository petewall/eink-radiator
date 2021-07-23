#!/bin/bash

# Change hostname
sudo sed --in-place --expression "s/raspberrypi/eink-radiator/" /etc/hostname /etc/hosts

# Update existing packages
sudo apt-get update
sudo apt-get upgrade --fix-missing
sudo apt-get remove python
sudo apt autoremove

# Install required software
sudo apt-get install git github-cli libjpeg8-dev python-numpy python-rpi.gpio python3 python3-numpy python3-pip python3-rpi.gpio vim

sudo reboot

# Install pipenv
pip3 install pipenv

# Download the repository
gh repo clone petewall/eink-radiator
cd eink-radiator

# Sync dependencies
~/.local/bin/pipenv sync

