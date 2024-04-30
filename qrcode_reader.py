#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
# import cv2
from PIL import Image
from pyzbar.pyzbar import decode

if __name__ == "__main__":
  qrcodefilepath = "./qrcode10.jpeg"
  # print(f"opencv version: {cv2.__version__}")
  print(f"reading test qr code at {qrcodefilepath}...")
  data = decode(Image.open(qrcodefilepath))
  print(f"decoded qr code data:\n{data}")

