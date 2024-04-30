#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from picamera2 import Picamera2, Controls
from libcamera import controls

class pihqCamera:

  exposure_night = {
    "controls": {
      "NoiseReductionMode": controls.draft.NoiseReductionModeEnum.HighQuality,
      "AnalogueGain": 6,
      "ExposureTime": int(10 * 1_000_000), # 10s
      "FrameRate": 1/10, # per sec
      "AwbEnable": 0,
      "AeEnable": 0,
      "ColourGains": (4.0, 1.5) # red, blue
    },
    "configuration": {}
  }

  exposure_day = {
    "controls": {
      "NoiseReductionMode": controls.draft.NoiseReductionModeEnum.HighQuality,
      "AnalogueGain": 16,
      # "ExposureTime": int(1/500 * 1_000_000),
      "FrameRate": 5, # per sec
      "AwbEnable": 1,
      "AeEnable": 1,
      # "ColourGains": (4.0, 1.5) # red, blue
    },
    "configuration": {}
  }

  # exposure_scandoc = {
  #   "controls": {
  #     "NoiseReductionMode": controls.draft.NoiseReductionModeEnum.Off,
  #     "AnalogueGain": 16,
  #     "ExposureTime": int(1/250 * 1_000_000),
  #     "FrameRate": 1/5, # per sec
  #   },
  #   "configuration": {

  #   }
  # }

  def __init__(self):
    print("pihqCamera instance initializing with default night mode...")
    self.camera = Picamera2()
    config = self.camera.create_still_configuration(
      main={"size": (2160,2160), "format": "RGB888"},
      # lores={"size": (1024,1024), "format": "YUV420"},
      buffer_count=1,
      queue=True
    )
    self.camera.configure(config)
    self.set_day_mode()
    self.started = False
    time.sleep(2)

  def start(self):
    self.camera.start()
    self.started = True
  
  def stop(self):
    self.camera.stop()
    self.started = False

  def set_night_mode(self):
    self.camera.set_controls(pihqCamera.exposure_night["controls"])
    time.sleep(2)

  def set_day_mode(self):
    self.camera.set_controls(pihqCamera.exposure_day["controls"])
    time.sleep(2)

  def capture(self, filepath):
    if not self.started:
      print("Cameras needs to start before capture: starting...")
      self.start()
    print("camera capture request:")
    r = self.camera.capture_request()
    print("complete. saving...")
    # if os.path.exists(filepath):
    #   print("old jpg exists, removing...")
    #   os.remove(filepath)
    #   print("removal complete. continuing with save")
    try:  
      r.save("main", filepath)
    except Exception as e:
      print(f"save exception:{e}")
    print("releasing camera...")
    r.release()
    print("release complete.")
    return True
