#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, json
import time
from datetime import datetime
from datetime import date
from datetime import timezone
from astral.sun import sun
from astral import Observer

class DayNight():
  def __init__(self, lat, lon):
    self.lat = lat
    self.lon = lon
    self.observer = self.set_observer(lat, lon)
  
  def set_observer(self, lat, lon):
    observer = Observer(
      latitude = lat,
      longitude = lon,
      elevation = 0.0
    )
    return observer

  def get_today_events(self):
    todayutc = datetime.now(timezone.utc)
    s = sun(self.observer, date=todayutc, tzinfo="UTC")
    # print((
    #     f'Dawn:    {s["dawn"]}\n'
    #     f'Sunrise: {s["sunrise"]}\n'
    #     f'Noon:    {s["noon"]}\n'
    #     f'Sunset:  {s["sunset"]}\n'
    #     f'Dusk:    {s["dusk"]}\n'
    #     f'Now:     {todayutc.isoformat()}'
    # ))
    return s


  def is_day(self):
    format = "%Y-%m-%d %H:%M:%S.%f%z"
    events = self.get_today_events()
    now = datetime.now(timezone.utc)
    dawn = events["dawn"]
    dusk = events["dusk"]
    is_day = now < dusk and now > dawn
    # print(f"is it after dawn? {now > dawn}")
    # print(f"is it before dusk? {now < dusk}")
    print(f"is it day as far as a camera is concerned? {is_day}")
    return is_day


if __name__ == "__main__":
  dn = DayNight(44.6509, -63.5923)
  dn.is_day()



