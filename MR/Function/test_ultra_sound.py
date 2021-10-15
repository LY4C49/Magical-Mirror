# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 19:39:21 2021

@author: Peter
"""
import RPi.GPIO as GPIO
import time

Trig=9
Echo=11
infrand=13

res=19

GPIO.setmode(GPIO.BCM)

GPIO.setup(Trig,GPIO.OUT,initial=GPIO.LOW)

GPIO.setup(Echo,GPIO.IN)
GPIO.setup(infrand,GPIO.IN)
GPIO.setup(res,GPIO.OUT,initial=GPIO.LOW)


def checkdist():
    #发出触发信号
    GPIO.output(Trig,GPIO.HIGH)
    #保持10us以上（我选择15us）
    time.sleep(0.000015)
    GPIO.output(Trig,GPIO.LOW)
    while not GPIO.input(Echo):
            pass
    #发现高电平时开时计时
    t1 = time.time()
    while GPIO.input(Echo):
            pass
    #高电平结束停止计时
    t2 = time.time()
    #返回距离，单位为米
    return (t2-t1)*340/2

def detect_people():
    if GPIO.input(infrand)==GPIO.HIGH:
        return True
    else:
        return False

while True:
    
    people=detect_people()
    if people:
        
        print("有人")
    else:
        print("无人")
    
    time.sleep(2)





