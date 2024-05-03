import os, sys, signal

def killapp():
  print("killapp called")
  os.kill(os.getpid(), signal.SIGINT)
  time.sleep(10)
