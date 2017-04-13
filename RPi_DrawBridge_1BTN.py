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
LEDRED16 = 16
LEDYLW20 = 20
LEDGRN21 = 21
GPIO.setup(LEDRED16,GPIO.OUT)
GPIO.setup(LEDYLW20,GPIO.OUT)
GPIO.setup(LEDGRN21,GPIO.OUT)

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
    GPIO.output(LEDRED16,GPIO.LOW)
    GPIO.output(LEDYLW20,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(LEDYLW20,GPIO.LOW)
    GPIO.output(LEDGRN21,GPIO.HIGH)
    print "Road Way is Open and Water Way is Closed"
    return;
  if Open_Road == 'WaterWay':
    GPIO.output(LEDGRN21,GPIO.LOW)
    GPIO.output(LEDYLW20,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(LEDYLW20,GPIO.LOW)
    GPIO.output(LEDRED16,GPIO.HIGH)
    print "Road Way is Closed and Water Way is Open"
    return;

#Initialize the gates and lights.
print "Press CTL-C to exit at any time."
print "Opening Road Way"
Open_Road = 'RoadWay'
ChgLights(Open_Road)
RoadWay_Gate.start(10)
WaterWay_Gate.start(5)
gate_state = 2

try:
	while True:
		Road_Input = GPIO.input(PSHBTNPIN17)
		if Road_Input == True and gate_state == 1:
			print "Opening Road Way"
			Open_Road = 'RoadWay'
			ChgLights(Open_Road)
			RoadWay_Gate.start(10)
			WaterWay_Gate.start(5)
			gate_state = 2
			Road_Input = False
		if Road_Input == True and gate_state == 2:
			print "Opening Water Way"
			Open_Road = 'WaterWay'
			ChgLights(Open_Road)
			RoadWay_Gate.start(5)
			WaterWay_Gate.start(10)
			gate_state = 1
			Road_Input = False
except KeyboardInterrupt:
	print "Closing Road and Water Way.  Shutting System Down...."
	RoadWay_Gate.start(5)
	WaterWay_Gate.start(5)
	GPIO.output(LEDRED16,GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(LEDYLW20,GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(LEDGRN21,GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(LEDRED16,GPIO.LOW)
	GPIO.output(LEDYLW20,GPIO.LOW)
	GPIO.output(LEDGRN21,GPIO.LOW)
	time.sleep(0.1)

print "Good bye!"
GPIO.cleanup()
