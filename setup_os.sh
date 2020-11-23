#!/bin/bash

# Update existing packages
sudo apt-get update
sudo apt-get upgrade --fix-missing
sudo apt autoremove

# Install required software
sudo apt-get install git jq libatlas-base-dev libffi-dev libssl-dev python3-pip vim
pip3 install docker-compose yq

# Install docker
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker ${USER}

# Change hostname
sudo sed --in-place --expression "s/raspberrypi/eink-radiator/" /etc/hostname /etc/hosts

# Move the program files
cp -r /boot/eink-radiator /home/pi/

sudo reboot