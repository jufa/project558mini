# referenced by crontab on startup, make sure this is chmod executable:

#!/bin/bash

APP_ENTRY="cd /home/pi/project558mini;source ./env/bin/activate;python timelapse_capture.py"
echo AurorEye Bootloader
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin 
cd "$(dirname "$0")"
eval $APP_ENTRY

