# -*- coding: utf-8 -*-
"""
Created on Thu May 27 13:00:16 2021

@author: Peter
"""
import Adafruit_DHT
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

FOUT=19
FIN=26
GPIO.setup(FOUT,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(FIN,GPIO.IN)

sensor=Adafruit_DHT.DHT11

# Set GPIO sensor is connected to

dht=4

H='H.txt'
T='T.txt'

# Use read_retry method. This will retry up to 15 times to

# get a sensor reading (waiting 2 seconds between each retry).



# Reading the DHT11 is very sensitive to timings and occasionally

# the Pi might fail to get a valid reading. So check if readings are valid.
while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, dht)
    
    if humidity is not None and temperature is not None:
        
        while GPIO.input(FIN)==GPIO.HIGH:
            continue
        
        GPIO.output(FOUT,GPIO.HIGH)
        f=open(H,'w+')
        f.write(str(int(humidity)))
        f.close()
        
        f=open(T,'w+')
        f.write(str(int(temperature)))
        f.close()
        GPIO.output(FOUT,GPIO.LOW)
        
    
        print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
    
    else:
    
        print('Failed to get reading. Try again!')
    
    time.sleep(5)
    
    
    
    