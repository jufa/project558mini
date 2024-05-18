import os, sys, signal, time, json

def killapp():
  print("killapp called")
  os.kill(os.getpid(), signal.SIGINT)
  time.sleep(10)

def parse_picamera2_metadata(metadata=None):
  metadata["Bcm2835StatsOutput"] = None
  return json.dumps(metadata, indent=2)
  '''
  {
    "SensorTimestamp":1668059618000,
    "ExposureTime":1000,
    "SensorBlackLevels":(4096, 4096, 4096, 4096),
    "AnalogueGain":1.0,
    "FrameDuration":200000,
    "Lux":348.8616943359375,
    "AeLocked":false,
    "FocusFoM":682,
    "SensorTemperature":34.0,
    "DigitalGain":1.0,
    "ColourGains":(2.510904550552368, 1.656680941581726),
    "ColourTemperature":4000,
    "ColourCorrectionMatrix":(
      1.2358283996582031,
      -0.003271537134423852,
      -0.23255407810211182,
      -0.0001986709248740226,
      1.460523009300232,
      -0.46032363176345825,
      0.1452644020318985,
      0.14539510011672974,
      0.7093411684036255),
    "ScalerCrop":(508, 0, 3040, 3040)
  }
  '''
  
