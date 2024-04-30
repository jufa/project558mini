#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, json
import time
import math
from datetime import datetime
from datetime import timezone
import threading
import queue
from exif import Image
from pihq_camera import pihqCamera
from daynight import DayNight
import pause
import shutil
from picamserve import Webserver


class TimelapseCapture():

  def __init__(self):
    self.queue = None
    self.thread = None
    self.camera = pihqCamera()
    self.daynight = DayNight(44.6509, -63.5923)
    self.root = os.path.join("./", "captures")
    self.interval = 30
    self.sequence_data={
      "start":0,
      "end":0,
      "count":0,
      "folder":""
    }

  def log(self, message):
    print(f"TIMELAPSE: {message}")

  def create_day_folder(self, datetime_reference):
    folder_name = datetime.strftime(datetime_reference,"%Y-%m-%d") #'2024-04-29'
    path = os.path.join(self.root, folder_name)
    if os.path.exists(path):
      print(f"folder {path} exists. Continuing...")
    else:
      print(f"generating sequence folder {folder_name}...")
      try:
        os.mkdir(path)
        print("folder created")
      except Exception as e:
        print(f"Error: could not make sequence folder: {e}")
        sys.exit(1)

    self.sequence_data["folder"] = path


  def start_timelapse(self, interval=10):
    self.interval = interval
    # create target folder:
    self.create_day_folder(datetime.now())
    
    self.interval = interval # in seconds
    print(f"interval specified is {self.interval} sec")
    self.thread = threading.Thread(target=self.run)
    self.thread.daemon = False
    self.thread.start()

  def run(self):
    print("Timelapse: Run...")
    while True:
      print("timelpase: run: starting loop...")
      # get next interval to trigger:
      now = datetime.now().timestamp()
      remainder = now % self.interval
      till_next = self.interval - remainder
      next_time = datetime.fromtimestamp(now + till_next)
      # next_time = datetime.fromtimestamp(math.ceil(datetime.now().timestamp()/self.interval)*self.interval)
      if datetime.now().day != next_time.day:
        print("next image will be capture over day boundary, creating new day folder...")
        self.create_day_folder(next_time)
      print(f"pausing until {next_time}...")
      pause.until(next_time)
      print("end pause.")
      self.get_image()

  def stop_timelapse():
    print("Stopping timelapse...")
    self.thread.start()
    print("Done.")

  def get_image(self):
    self.log("\n-----------\ncapturing image...")
    # self.log(f"it is currently {'day' if self.daynight.is_day() else 'night'}")
    try:
      self.camera.capture("capture.jpg")
      self.log("capture complete")
    except Exception as e:
      self.log(f"ERROR: Capture: {e}")
     
    with open('capture.jpg', 'rb') as image:
      exif_data = Image(image)
      #  print(my_image.datetime) #'2024:04:29 20:52:55'
      filename = exif_data.datetime.replace(':','-').replace(' ','T') #'2024-04-29T20-52-55'
      
      filename += ".jpg"
      source = os.path.join("./", "capture.jpg")
      destination = os.path.join(self.sequence_data["folder"], filename)
      print(f"copying {source} to {destination}...")
      
      try:
        shutil.copy(source, destination)
        print("File copied successfully.")
      except Exception as e:
        print(f"Error: could not copy file: {e}")
       

       


  def setup(self):
    self.log('setup: start_server()')
    time.sleep(1) # cannot start up bottle immediately, needs some wifi setup time
    self.start_server()
    data = {}

  def read(self):
    # in this case when we want to read changes in state of the interface
    #  feels like we may be shoehoming here, i.e. polling versus async/event driven
    return self.data

  def update_status(self, status):
    """
    This is called by main to inject overal Auroreye status object for use in the webserver interface display
    """
    self.status = status

  def start(self):
    self.log("start webserver for access point")

    
  def stop(self):
    self.log("webserver for access point shutting down...")
    # self.server.stop()

if __name__ == "__main__":
  print("initializing webserver instance...")
  webserver = Webserver()
  print("webserver instantiated.")
  print("starting webserver...")
  webserver.start()
  print("webserver started.")
  print("timelapse instantiating...")
  timelapse = TimelapseCapture()
  print("timelapse instantiated.")
  print("starting timelapse...")
  timelapse.start_timelapse(interval=30)
