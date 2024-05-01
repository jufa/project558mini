#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from picamera2 import Picamera2, Controls
from libcamera import controls
import cv2

class pihqCamera:

  exposure_night = {
    "controls": {
      "NoiseReductionMode": controls.draft.NoiseReductionModeEnum.HighQuality,
      "AnalogueGain": 4,
      "ExposureTime": int(10 * 1_000_000), # 10s
      "FrameRate": 1/10, # per sec
      "AwbEnable": 0,
      "AeEnable": 0,
      "ColourGains": (4.0, 1.5), # red, blue
      "Saturation": 0.5
    },
    "configuration": {}
  }

  exposure_day = {
    "controls": {
      "NoiseReductionMode": controls.draft.NoiseReductionModeEnum.HighQuality,
      "AnalogueGain": 1,
      # "ExposureTime": int(1/500 * 1_000_000),
      "FrameRate": 5, # per sec
      "AwbEnable": 1,
      "AwbMode": controls.AwbModeEnum.Daylight,
      "AeEnable": 1,
      # "AeMeteringMode": controls.AeMeteringModeEnum.Spot,
      "AeConstraintMode": controls.AeConstraintModeEnum.Highlight,
      "Saturation": 0.5,
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
      lores={"size": (512,512), "format": "YUV420"},
      buffer_count=2,
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

  def capture(self, filepath, filepath_lores=None):
    if not self.started:
      print("Cameras needs to start before capture: starting...")
      self.start()
    print("camera capture request:")
    r = self.camera.capture_request()
    print("complete. saving...")
    try:  
      r.save("main", filepath)
      if filepath_lores:
        lres = r.make_image("main", 540, 540) # PIL image from this CompletedRequest object at 1/4 UHD resolution
        lres.save(filepath_lores)
    except Exception as e:
      print(f"save exception:{e}")
    print("releasing camera...")
    r.release()
    print("release complete.")
    return True
