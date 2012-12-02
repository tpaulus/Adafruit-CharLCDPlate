#!/usr/bin/python

# Written by Tom Paulus, @tompaulus

import spidev
import time
import os
import RPi.GPIO as GPIO
from Adafruit_CharLCDPlate import Adafruit_CharLCD as LCD

#GPIO and SPI Initialization
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
spi = spidev.SpiDev()
spi.open(0, 0)

#For Menu State
state = 1
current = 0

#ADC Ports
pot_adc = 0
light_adc = 6
print "Press CTRL+Z to exit"


def readadc(adcnum):
    """This Function reads the port defined, and returns an analogue value"""
    if (adcnum > 7) or (adcnum < 0):
        return -1
    r = spi.xfer2([1, (8 + adcnum) << 4, 0])
    adcout = ((r[1] & 3) << 8) + r[2]
    return adcout

def m1(pot, light):
    """The Default/Home Menu Screen"""
    lcd.message('Pot:' + pot + '\nLight:' + light)

def m2(pot):
    """ This menu shows only Potentiometer related information """
    percent0 = (int(pot)/10.23)
    percent0 = "%0.2f" % percent0
    lcd.message('Potentiometer:\n' + pot + "   " + percent0 + '% ')

def m3(light):
    """ This menu show onlt light sensor related information """
    percent1 = (int(light)/10.23)
    percent1 = "%0.2f" % percent1
    lcd.message('Light Level:\n' + light + '   ' + percent1+ '% ')

#initialize and clear the LCD
lcd = LCD(15, 13, [12, 11, 10, 9], 14)
lcd.clear()

while True:
    #set the cursor to the origin position
    lcd.home()
    #read the level of the pot and light sensors connected to the ADC
    pot_level = readadc(pot_adc)
    light_level = readadc(light_adc)
    #Convert the values to only 4 digits, and pad with 0s if necessary
    pot_level = "%04d" % pot_level
    light_level = "%04d" % light_level
    current = state #save the current state
    #read the buttons below the display, and change the menu accordingly
    if lcd.input(lcd.UP):
        state += 1
    if lcd.input(lcd.DOWN):
        state -= 1
    if lcd.input(lcd.SELECT):
        state = 1
    if state == 0:
        state = 3
    if state == 4:
        state = 1

    #If the menu has changed, clear the display
    if state != current:
        lcd.clear()

    #Use the state number to execute a function
    if state == 1:
        m1(pot_level, light_level)
    if state == 2:
        m2(pot_level)
    if state == 3:
        m3(light_level)

    #Wait .1 seconds
    time.sleep(.1)