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
    self.camera.post_callback = self.post_callback
    self.camera.pre_callback = self.pre_callback
    self.daynight = DayNight(44.6509, -63.5923)
    self.root = os.path.join("./", "captures")
    self.interval = 30
    self.is_night = True
    self.sequence_data={
      "start":0,
      "end":0,
      "count":0,
      "folder":""
    }


  def pre_callback(self, request):
    print("pre_callback called")

  def post_callback(self, request):
    print("post_callback called")

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
    self.interval = interval # in seconds
    print(f"interval specified is {self.interval} sec")
    self.thread = threading.Thread(target=self.run)
    self.thread.daemon = False
    self.thread.start()

  def wait_till_boundary(self):
    boundary = 10 # sec
    now = datetime.now().timestamp()
    remainder = now % boundary #todo this is a hack fro checking the synchronization times. it appeasr the cam free runs capture, capture_image does not trigger a new capture, just grabs either the one almost done or the next one starting after the request.
    till_next = boundary - remainder
    next_time = datetime.fromtimestamp(now + till_next)
    print(f"pausing until {next_time}...")
    pause.until(next_time)
    print(f"pausing complete. continuing.")

  def set_day_night(self):
    print("set_day_night: checking if day or night...{}")
    if not self.daynight.is_day():
      print("it is night. Setting camera to night mode...")
      self.camera.set_night_mode()
      self.is_night = True
      print("complete.")
    elif self.daynight.is_day():
      print("it is day. Setting camera to day mode...")
      self.camera.set_day_mode()
      self.is_night = False
      print("complete.")
    else:
      print(f"conditional fallthrough: daynight not reportingis_day as bool: output: {self.daynight.is_day()}")


  def run(self):
    print("Timelapse: Run...")
    self.set_day_night()

    while True:
      print("timelpase: run: starting loop...")
      # get next interval to trigger:
      if not self.camera.started:
        # wait till ten second boundary...
        self.wait_till_boundary()
        print("end pause.")
      if not self.is_night:
        self.wait_till_boundary() # daytime camera is freerunning at a framerate higher than our timelapose framerate in order to do Aeb Awb calcs. so we make it wait till a boundary
      print(f"getting image at {datetime.now()}")
      self.get_image()
      print(f"image capture complete at {datetime.now()}")

  def stop_timelapse():
    print("Stopping timelapse...")
    self.thread.start()
    print("Done.")

  def get_image(self):
    self.log("\n-----------\ncapturing image...")
    self.log(f"it is currently {'day' if self.daynight.is_day() else 'night'}")
    if self.is_night and self.daynight.is_day():
      print("transition to day time exposure settings...")
      self.camera.set_day_mode()
      self.is_night = False
      print("complete.")
    elif not self.is_night and not self.daynight.is_day():
      print("transition to night time exposure settings...")
      self.camera.set_night_mode()
      self.is_night = True
      print("complete.")

    try:
      self.camera.capture("capture.jpg", "capture_lores.jpg")
      self.log("capture complete")
    except Exception as e:
      self.log(f"ERROR: Capture: {e}")
     
    with open('capture.jpg', 'rb') as image:
      exif_data = Image(image)
      #  print(my_image.datetime) #'2024:04:29 20:52:55'
      self.create_day_folder(datetime.now())
      filename = exif_data.datetime.replace(':','-').replace(' ','T') #'2024-04-29T20-52-55'
      filename += "-NIGHT" if self.is_night else "-DAY"
      filename += ".jpg"
      source = os.path.join("./", "capture.jpg")
      destination = os.path.join(self.sequence_data["folder"], filename)
      print(f"copying {source} to {destination}...")
      
      try:
        shutil.copy(source, destination)
        print("File copied successfully.")
      except Exception as e:
        print(f"Error: could not copy file: {e}")


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
