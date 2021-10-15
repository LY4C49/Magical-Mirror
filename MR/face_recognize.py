# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 19:15:55 2021

@author: Peter
"""
from aip import AipFace
from picamera import PiCamera
import urllib.request
import RPi.GPIO as GPIO
import base64
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

#百度人脸识别API账号信息
APP_ID = '22712501'
API_KEY = 'xH9EwQM5c9QkQly8LiijBUVU'
SECRET_KEY ='z3nQf7Vu8GjglfNDDmWxfocX6FQK5NFk'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)#创建一个客户端用以访问百度云
#图像编码方式
IMAGE_TYPE='BASE64'
camera = PiCamera()#定义一个摄像头对象
#用户组
GROUP = '616'




#照相函数
def getimage():
    camera.resolution = (1024,768)#摄像界面为1024*768
    camera.start_preview(alpha=0)#开始摄像
    camera.capture('faceimage.jpg')#拍照并保存

#上传到百度api进行人脸检测
def transimage():
    f = open('faceimage.jpg','rb')
    img = base64.b64encode(f.read())
    return img

def go_api(image):
    result=client.search(str(image, 'utf-8'), IMAGE_TYPE, GROUP);#在百度云人脸库中寻找有没有匹配的人脸
    if result['error_msg']=='SUCCESS':#如果成功了
        name=result['result']['user_list'][0]['user_id']#获取名字
        score = result['result']['user_list'][0]['score']#获取相似度
        if score>80:
            print("welcome%s !"%name)
            f=open('name.txt','w+')
            f.write(name)
            f.close()
            return 1
        else:
             print("I do not konw you!")
             name='STRANGER'
             return 0
    if result['error_msg']=='pic not has face':
        print('did not detect any face!')
        return 0
    else:
        print(result['error_code']+' ' + result['error_code'])
        return 0

def detect_people():
    if GPIO.input(infrand)==GPIO.HIGH:
        print("people")
        return True
    else:
        print("no people")
        return False

while True:
    print("start")
    people=detect_people()
    if people:
        getimage()
        img=transimage()
        result=go_api(img)
        if result==1:
            GPIO.output(res,GPIO.HIGH)
            while True:
                people=detect_people()
                if people==True:
                    time.sleep(3)
                    continue
                else:
                    break
            time.sleep(3)
        else:
            GPIO.output(res,GPIO.LOW)
    else:
        GPIO.output(res,GPIO.LOW)
    print("end")
    time.sleep(2)
        

