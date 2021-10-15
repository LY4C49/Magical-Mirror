# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 21:58:46 2021

@author: Peter
"""
import pygame
import sys
import random
#sys.path.append("/media/pixelchen/OS/Users/chen/source/repos/赵小姐的魔镜/")
import os
import time
from Function import Time,Fun
#import QR
from pygame.locals import *
import pygame.freetype

FPS=30
pygame.init()
screen = pygame.display.set_mode((1080, 1920), FULLSCREEN)
pygame.display.set_caption("MagicMirror")
clock=pygame.time.Clock()
ZhuanLanTitle=''
Hot=[]

def showTime():
    # Lunar=Fun.getLunar()
    # Holiday=Fun.getHoliday()
    font = pygame.freetype.Font('./FontLib/setup/苹方黑体-中粗-简.ttf', 192)
    FormatTime = Time.getTime()
    font.render_to(screen, (50, 100), FormatTime, (255, 255, 255), 20)  # 时间

    year = str(Time.getYear())
    month = str(Time.getMonth())
    day = str(Time.getDay())
    XingQi = Time.getWeekday()
    Date = year + '年' + month + '月' + day + '日' + '    ' + XingQi  # 日期
    dateFont = pygame.freetype.Font('./FontLib/setup/苹方黑体-准-简.ttf', 36)
    dateFont.render_to(screen, (100, 260), Date, (255, 255, 255), 10)
    dateFont.render_to(screen, (110, 300), Lunar, (255, 255, 255), 10)

    HolidayIcon=pygame.image.load("FunIcon/Holiday.png")
    HolidayIconRect=HolidayIcon.get_rect()
    HolidayIconRect.center=(100,400)

    newRect=HolidayIconRect.inflate(24,24)
    dateFont.render_to(screen,(220,380),Holiday,(255,255,255),20)
    screen.blit(HolidayIcon,HolidayIconRect)

Hot=Fun.getHot()
def showHot():#百度热搜以及知乎专栏
    NameFont=pygame.freetype.Font("FontLib/setup/苹方黑体-中粗-简.ttf",36)
    NameFont.render_to(screen,(50,250+225),'实时热点',(255,255,255),10)
    HotFont=pygame.freetype.Font("FontLib/setup/苹方黑体-准-简.ttf",24)
    for i in range(3):
        HotFont.render_to(screen,(50,225+300+i*25),Hot[i],(255,255,255),10-2*i)
    pygame.draw.line(screen,(255,255,255),(50,1590),(520,1590))#分隔线
    QRPic=pygame.image.load("QR/QR.png")
    QRPic=pygame.transform.scale(QRPic,(225,225))
    QRPicRect=QRPic.get_rect()
    QRPicRect.center=(900,1700)
    screen.blit(QRPic,QRPicRect)
    NameFont.render_to(screen,(50,225+400),"知乎日报："+'『'+ZhuanLanTitle+'』',(255,255,255),10)
    HotFont.render_to(screen,(810,1680-130),"扫描以阅读日报",(255,255,255),10)
    
    
showHot()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    FormatDate = Time.getDate()
    screen.fill((0, 0, 0),rect=(0,0,580,450))#需要实时刷新的其实就只有时间
    if Time.getMinute()==0 and Time.getSec()==0:#整点更新API数据
        updateAPI()
        screen.fill((0,0,0))
        showHot()

    showTime()
    clock.tick(FPS)
    pygame.display.update()


# =============================================================================
# 注册了聚合数据
# 搞定了显示节日功能
# 搞定了显示热点功能
#注意：热点原大小超出了屏幕范围，必须根据实际调整！
# =============================================================================
