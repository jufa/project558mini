#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, json
import time
from datetime import datetime
from datetime import date
import RPi.GPIO as GPIO
import threading

class StatusLed():
  def __init__(self):
    self.thread = None
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.OUT)
    self.led_status = 1
    self.blinks_left = 0

    self.thread = threading.Thread(target=self.run)
    self.thread.daemon = False
    self.thread.start()

  def led_on(self):
    GPIO.output(16, GPIO.LOW)

  def led_off(self):
    GPIO.output(16, GPIO.HIGH)

  def run(self):
    while True:
      time.sleep(0.3)
      if self.blinks_left > 0:
        self.blinks_left -= 1
        self.led_off() if self.led_status == 1 else self.led_on()

  def blink(self, count=1):
    self.blinks_left = count

if __name__ == "__main__":
  sled = StatusLed()
  sled.blink(50)



