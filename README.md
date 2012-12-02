Adafruit-CharLCDPlate
=====================

My Improvements to the Adafruit CharLCDPlate Library

Added a simple, lcd.input function, which removes the need for the user to import the MCP23017 library.

Also, the user no longer needs to add a not before each button statement, because it is now found in the function input().

Included is the program ADC_Display.py, which is my demo/test file which uses a MCP3008 to read the level of a Potentiometer and a Light Sensor and displays them on a display in various menus.