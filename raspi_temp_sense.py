# A program to test the raspberry pi's capabilities
# with the DHT11 temperature sesnsor this program
# will then write sensor data to server

# GPIO 18 corresponds to pin 24 on PI this is used to toggle LED
# Pin 16 in def read_data is used to read the data from the temp/humid sensor

import RPi.GPIO as GPIO
from bottle import route, run
from time import sleep
import Adafruit_DHT

@route('/test')
# route to test that connection is possible
def test():
        return 'test is a success'

@route('/read_data',method='GET')
# a route that returns a dictionary of temperature
# and humidity values
def read_data():
        Humidity, Temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 16)
        dict = {
                "node": 1,
                "humidity": Humidity,
                "temperature": Temperature,
                "location": "tbd"
                }
        return dict

@route('/ledctrl')
# a route that toggles a led on the pi
def ledctrl():
        global ledctrl
        ledctrl = not ledctrl
        GPIO.output(18, not GPIO.input(18))
        return 'LED toggled'

# GPIO Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18,False)
