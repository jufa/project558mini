# project558mini

This is a project to make a compact, off the shelf, day/night all sky camera timelapse generator primarily for aurora capture using the following Hardware:

## Hardware
 - Raspberry Pi Zero 2W (or other v3 and higher Pi with wifi)
 - Raspberry Pi High Quality Camera
 - Fisheye lens (180 degree) or narrow field camera for specific horizons
 - WIFI netowrk

## Features:
 - Day auto exposure and night time fixed exposure with automatic transition
 - rudimentary web page to monitor current imagery
 - compact and low power consumption
 - hardware fits inside a 5.5" acryllic dome
 - no additional custom PCBs required
 - RGB capture, adjustable exposure, gains, color balance
 - possible to use No-IR filder cameras or monochromatic with or without line filters
 - time sync thorugh wifi
 - startup at boot, hands-off
 - can set up remote SSH access via rasperry pi connect (like VNC but free)
 - app watchdog to auto reboot in case of lock up
 - Specific config/settings for long exposure timelap[se with the raspberry pi HQ camera

## to use
 - create installation image via RPI Imager of default RPI zero 2W 64-bit lite Raspbian OS
 - `sudo apt update`
 - `sudo apt install git`
 - `sudo apt install libgl1`
 - `sudo apt install -y python3-dev build-essential libcap-dev`
 - `sudo apt install -y libcamera-dev python3-libcamera libcamera-apps`
 - `git clone https://github.com/jufa/project558mini.git`
 - `sudo apt install python3-pip`
 - `python -m venv /path/to/venv --system-site-packages`
 - `source env/bin/activate`
 - `mkdir 'captures'`
 - `pip install -r requirements.txt`
 - `pip install opencv-python`
 - `pip install exif`
 - `pip install git+https://github.com/raspberrypi/picamera2.git`
 - set up the crontab file as per the example file
 - put repo in /home/pi/project558mini or similar (updating crontab appropriately)
 - install python packages as per requirements.txt
