#! /usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep
import datetime
import requests

GPIO.setmode(GPIO.BCM)

# GPIO Pin of the component
lightPin = 18
buttonPin = 17

startTime = None
endTime = None

GPIO.setup(lightPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.output(lightPin, True)
sleep(.3)
GPIO.output(lightPin, False)
sleep(.3)
GPIO.output(lightPin, True)
sleep(.2)
GPIO.output(lightPin, False)
sleep(0.2)
GPIO.output(lightPin, True)
sleep(1)
GPIO.output(lightPin, False)

inputStatus = GPIO.input(buttonPin)

print("Standing Time Tracking System has been activated...")
try:

  while True:
    if inputStatus !=GPIO.input(buttonPin):
      inputStatus = GPIO.input(buttonPin)
      GPIO.output(lightPin, not GPIO.input(buttonPin))
      if inputStatus == True:
        print("input changed to false")
        endTime = datetime.datetime.now()
	print("Start At: {:s}, End At: {:s}".format(str(startTime), str(endTime)) )
	difference = endTime - startTime
        minutes, seconds = divmod(difference.days * 86400 + difference.seconds, 60)
	print("duration Minutes: {:d}, Seconds: {:d}").format(minutes, seconds)
	r = requests.post("https://secure-chamber-61971.herokuapp.com/create", data={'start_at': str(startTime), 'end_at': str(endTime)})
	print(r.status_code)
      else:
        print("input changed to true")
        startTime = datetime.datetime.now()
    sleep(1)
finally:
  GPIO.output(lightPin, False)
  GPIO.cleanup()
  print("Standing Time Tracking System stopped.")
