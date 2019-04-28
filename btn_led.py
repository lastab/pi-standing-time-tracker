#! /usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep
import datetime
import requests

GPIO.setmode(GPIO.BCM)

lightPin = 17
buttonPin = 4

startTime = datetime.datetime.now()
endTime = None

led_bulb = False

GPIO.setup(lightPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

inputStatus = GPIO.input(buttonPin)
previousInputStatus = GPIO.input(buttonPin)

print("Standing Time Tracking System has been activated...")
try:

  while True:
    inputStatus = GPIO.input(buttonPin)
    # if input status changed
    if inputStatus != previousInputStatus:
      previousInputStatus = inputStatus
      if inputStatus == True:
        # if pressure plate is no pressed
        print("input changed to false")
        endTime = datetime.datetime.now()
        print("Start At: {:s}, End At: {:s}".format(str(startTime), str(endTime)) )
        difference = endTime - startTime
        minutes, seconds = divmod(difference.days * 86400 + difference.seconds, 60)
        print("duration Minutes: {:d}, Seconds: {:d}").format(minutes, seconds)
        try:
          r = requests.post("https://secure-chamber-61971.herokuapp.com/end", data={'start_at': str(startTime), 'end_at': str(endTime)})
          print(r.status_code)
        except:
          print("Post request failed.")
      else:
        # if pressure plate pressed
        print("input changed to true")
        startTime = datetime.datetime.now()

        # Turn on LED
        GPIO.output(lightPin, True)

        try:
          r = requests.post("https://secure-chamber-61971.herokuapp.com/start", data={'start_at': str(startTime)})
          print(r.status_code)
        except:
          print("Post request failed.")


    # Blink led if swithc is turned off
    if inputStatus == True:
      led_bulb = not led_bulb
      GPIO.output(lightPin, led_bulb)

    # Sleep
    sleep(1)

finally:

  GPIO.output(lightPin, False)
  GPIO.cleanup()

  print("Standing Time Tracking System stopped.")
# The end
