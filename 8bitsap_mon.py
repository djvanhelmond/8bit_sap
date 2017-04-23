#!/usr/bin/env python
import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM)  

# 4 - clock
# 5 - SIG:halt
# 24 - NONE

pins = [4, 5, 24]
for pin in pins:
  GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

class sap1_io():
  def __init__(self):
    self.halt = False # GPIO # 5

  def read_io(self):
    self.halt = GPIO.input(5)


class tickcounter():
  def __init__(self):
    from time import time
    now = time()
    self.total_ticks = 0
    self.Hz = 0.0
    self.tick_per_sec = 0
    self.tick_time = now

  def tick(self):
    self.total_ticks += 1
    self.tick_per_sec += 1
    self.calc_Hz()
    sapio.read_io()

  def calc_Hz(self):
    from time import time
    now = time()
    delta = now - self.tick_time
    if delta > 1:
      self.Hz = self.tick_per_sec / delta
      #self.Hz = (self.Hz + (self.tick_per_sec / delta)) / 2
      self.tick_time = now
      self.tick_per_sec = 0

ticker = tickcounter()
sapio = sap1_io()

def my_callback(channel):
  global ticker
  global sapio
  ticker.tick()
  print("Clock tick: {:10d} detected. Speed: {:7.2f} Hz --- H:{} ...".format(ticker.total_ticks, ticker.Hz, sapio.halt))
  
GPIO.add_event_detect(4, GPIO.FALLING, callback=my_callback)
  
try:  
  GPIO.wait_for_edge(24, GPIO.RISING)  
except KeyboardInterrupt:
  GPIO.cleanup()       # clean up GPIO on CTRL+C exit   
GPIO.cleanup()           # clean up GPIO on normal exit  

