#Author:  Peter Di Giorgio
#Date: 09042017
#Version: 1.0
#Purpose: Drawbridge script for BSidesAugusta STEM.  This script is 
#written for a single button which controls two PWM Servos.  LEDs
#will change color to indicate the traffic flow of the Road Way.
#It is assumed that the Water Way traffic will see the position
#of the gate.


import RPi.GPIO as GPIO
import time

#Set the GPIO mode for BCM numbering
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Input Pins
PSHBTNPIN17 = 17
GPIO.setup(PSHBTNPIN17,GPIO.IN,pull_up_down=GPIO.PUD_UP)

#Output Pins
LEDPIN16 = 16
LEDPIN20 = 20
LEDPIN21 = 21
GPIO.setup(LEDPIN16,GPIO.OUT)
GPIO.setup(LEDPIN20,GPIO.OUT)
GPIO.setup(LEDPIN21,GPIO.OUT)

#Output PWM: GPIO12, GPIO18
servoPINRW = 12
servoPINWW = 13
GPIO.setup(servoPINRW,GPIO.OUT)
GPIO.setup(servoPINWW,GPIO.OUT)

#Set 50 Hz
RoadWay_Gate = GPIO.PWM(servoPINRW,50)
WaterWay_Gate = GPIO.PWM(servoPINWW,50)

#Start servos at full left position or both gates down
RoadWay_Gate.start(5)
WaterWay_Gate.start(5)

#Function to change lights
def ChgLights (Open_Road):
  if Open_Road == 'RoadWay':
    GPIO.output(LEDPIN16,GPIO.LOW)
    GPIO.output(LEDPIN20,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(LEDPIN20,GPIO.LOW)
    GPIO.output(LEDPIN21,GPIO.HIGH)
    print "Road Way is Open and Water Way is Closed"
    return;
  if Open_Road == 'WaterWay':
    GPIO.output(LEDPIN21,GPIO.LOW)
    GPIO.output(LEDPIN20,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(LEDPIN20,GPIO.LOW)
    GPIO.output(LEDPIN16,GPIO.HIGH)
    print "Road Way is Closed and Water Way is Open"
    return;

#Initialize the gates and lights.
print "Press CTL-C to exit at any time."
print "Opening Road Way"
Open_Road = 'RoadWay'
ChgLights(Open_Road)
RoadWay_Gate.start(10)
WaterWay_Gate.start(5)

try:
	while True:
		Road_Input = GPIO.input(PSHBTNPIN17)
		if Road_Input == True and Open_Road == 'WaterWay':
			print "Opening Road Way"
			Open_Road = 'RoadWay'
			ChgLights(Open_Road)
			RoadWay_Gate.start(10)
			WaterWay_Gate.start(5)
		if Road_Input == True and Open_Road == 'RoadWay':
			print "Opening Water Way"
			Open_Road = 'WaterWay'
			ChgLights(Open_Road)
			RoadWay_Gate.start(5)
			WaterWay_Gate.start(10)
except KeyboardInterrupt:
	print "Closing Road and Water Way.  Shutting System Down...."
	RoadWay_Gate.start(5)
	WaterWay_Gate.start(5)
	GPIO.output(LEDPIN16,GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(LEDPIN20,GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(LEDPIN21,GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(LEDPIN16,GPIO.LOW)
	GPIO.output(LEDPIN20,GPIO.LOW)
	GPIO.output(LEDPIN21,GPIO.LOW)
	time.sleep(0.1)

print "Good bye!"
GPIO.cleanup()
