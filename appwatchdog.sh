#!/bin/sh
echo "check service $(date)" >> /home/pi/project558mini/logs/timelapse_capture.log
ps auxw | grep timelapse_capture.py | grep -v grep > /dev/null
if [ $? != 0 ]
then
        echo "timelapse_capture process not runnning. Rebooting at $(date)" >> /home/pi/project558mini/logs/timelapse_capture.log
        echo "warning reboot is disabled during devlopment" >> /home/pi/project558mini/logs/timelpase_capture.log
        #sudo reboot now >> /home/pi/project558mini/logs/timelapse_capture.log
else 
        echo "timelapse_capture.py is running"  >> /home/pi/project558mini/logs/timelapse_capture.log
fi
