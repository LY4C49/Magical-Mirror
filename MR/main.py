# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 14:29:20 2021

@author: Peter
"""
import pygame
import sys
import random
import RPi.GPIO as GPIO
import os
import time
from Function import Time,Fun,agenda,topque,Weather
from pygame.locals import *
import pygame.freetype

# 有没有人的标记
people=26
GPIO.setmode(GPIO.BCM)
GPIO.setup(people,GPIO.IN)

FPS=30
pygame.init()
screen = pygame.display.set_mode((1080, 1920), FULLSCREEN)
#screen = pygame.display.set_mode((1080, 1920))
pygame.display.set_caption("MagicMirror")
clock=pygame.time.Clock()

Zhihu=topque.GetTopQue()
Hot=Fun.getHot()
# agenda=agenda.GetAgenda()
Lunar=Fun.getLunar()
Holiday=Fun.getHoliday()



def showTime():
    font = pygame.freetype.Font('./FontLib/setup/苹方黑体-中粗-简.ttf', 192)
    FormatTime = Time.getTime()
    font.render_to(screen, (50+300, 100), FormatTime, (255, 255, 255), 20)  # 时间

    year = str(Time.getYear())
    month = str(Time.getMonth())
    day = str(Time.getDay())
    XingQi = Time.getWeekday()
    Date = year + '年' + month + '月' + day + '日' + '    ' + XingQi  # 日期
    dateFont = pygame.freetype.Font('./FontLib/setup/苹方黑体-准-简.ttf', 36)
    dateFont.render_to(screen, (100+300, 260), Date, (255, 255, 255), 10)
    dateFont.render_to(screen, (110+300+50, 320), Lunar, (255, 255, 255), 10)

    HolidayIcon=pygame.image.load("FunIcon/Holiday.png")
    HolidayIconRect=HolidayIcon.get_rect()
    HolidayIconRect.center=(180+300,400)

    newRect=HolidayIconRect.inflate(24,24)
    dateFont.render_to(screen,(220+300,380),Holiday,(255,255,255),20)
    screen.blit(HolidayIcon,HolidayIconRect)

def showHot():#百度热搜以及知乎热搜
    NameFont=pygame.freetype.Font("FontLib/setup/楷体.TTF",36+18)
    NameFont.render_to(screen,(50,475+50),'实时热点',(255,255,255),10)
    HotFont=pygame.freetype.Font("FontLib/setup/楷体.TTF",24+6)
    for i in range(3):
        HotFont.render_to(screen,(50,525+65+i*(25+10)),Hot[i],(255,255,255),10)
    pygame.draw.line(screen,(255,255,255),(50,625+50+50),(250,625+50+50))#分隔线
    
    NameFont=pygame.freetype.Font("FontLib/setup/楷体.TTF",36+18)
    NameFont.render_to(screen,(50,650+100),'知乎热榜',(255,255,255),10)
    HotFont=pygame.freetype.Font("FontLib/setup/楷体.TTF",24+6)
    for i in range(1,4):
        HotFont.render_to(screen,(50,680+100+i*(25+10)),Zhihu[i],(255,255,255),10)
    pygame.draw.line(screen,(255,255,255),(50,800+50+100),(250,800+50+100))#分隔线
    
def showAgenda(Agenda):
    NameFont=pygame.freetype.Font("FontLib/setup/楷体.TTF",36+18)
    NameFont.render_to(screen,(650,600),'备忘录Top5',(255,255,255),30)
    HotFont=pygame.freetype.Font("FontLib/setup/楷体.TTF",24+12)
    if len(Agenda)>=5:
        for i in range(5):
            HotFont.render_to(screen,(675,675+i*40),Agenda[i],(255,255,255),30)
            #pygame.draw.line(screen,(255,255,255),(650,800),(900,800))#分隔线
    else:
        for i in range(len(Agenda)):
            HotFont.render_to(screen,(675,675+i*40),Agenda[i],(255,255,255),30)
            #pygame.draw.line(screen,(255,255,255),(650,900),(900,900))#分隔线
def showerr():
    NameFont=pygame.freetype.Font("FontLib/setup/楷体.TTF",36+18)
    NameFont.render_to(screen,(675,675),'Warning! 网络可能开小差了！',(255,255,255),30)

# =============================================================================
# 天气部分开始

# 注意：以下为天气显示部分
# 树莓派可能有其特殊性，所以必须注意所有从网页获取信息的代码禁止放入显示模块
#PS：树莓派好像要一直show才行
#每15mins更新一下网页内容！
currentTemp=Weather.getCurrentWeather()
WeatherMessage=Weather.getWeather()
SuggestionMessage =Weather.getSuggestion()


def getWeatherIcon(WeatherCode, size):
    fileName = WeatherCode + '@' + str(size) + 'x' + '.png'
    wholePath = 'WeatherIcon/black/' + fileName
    icon = pygame.image.load(wholePath)
    return icon

def showMainWeather():
    if Time.getHour() in range(5, 18):
        TodayDayIcon = getWeatherIcon(WeatherMessage['TodayInfo']['日间天气代码'], 2)
        TodayDayIconRect = TodayDayIcon.get_rect()
        TodayDayIconRect.left = 820-330
        TodayDayIconRect.top = 1110+50
        screen.blit(TodayDayIcon, TodayDayIconRect)

        WeatherFont = pygame.freetype.Font('FontLib/setup/楷体.TTF', 32)
        WeatherFont.render_to(screen, (948-330, 1100+50), WeatherMessage['TodayInfo']['日间天气'],(255,255,240),10)

        NightFont=pygame.freetype.Font('FontLib/setup/楷体.TTF', 24)
        NightFont.render_to(screen, (888-330, 1325+50), '夜间:'+WeatherMessage['TodayInfo']['夜间天气'], (65,105,225), 10)
    else:
        TodayNightIcon = getWeatherIcon(WeatherMessage['TodayInfo']['夜间天气代码'], 2)
        TodayNightIconRect = TodayNightIcon.get_rect()
        TodayNightIconRect.left = 820-330
        TodayNightIconRect.top = 1110+50
        screen.blit(TodayNightIcon, TodayNightIconRect)

        WeatherFont = pygame.freetype.Font('FontLib/setup/楷体.TTF', 48)
        WeatherFont.render_to(screen, (948-330, 1100+50), WeatherMessage['TodayInfo']['夜间天气'],(255,255,240),10)

    city=WeatherMessage['City']
    cityFont=pygame.freetype.Font('FontLib/setup/楷体.TTF',32)
    cityFont.render_to(screen,(630+48-330,1100+50+50),city+'市',(255,255,255),10)

    Point=pygame.image.load("FunIcon/Point.png")
    PointRect=Point.get_rect()
    PointRect.left=590+48-330
    PointRect.top=1100+50+50
    screen.blit(Point,PointRect)

    humiPic=pygame.image.load("WeatherIcon/Humi64.png")
    humiPicRect=humiPic.get_rect()
    humiPicRect.left=960-330
    humiPicRect.top=1133+50
    screen.blit(humiPic,humiPicRect)

    if int(currentTemp)<20:
        COLOR=(135,206,250)
    elif int(currentTemp)<27 :
        COLOR=(127,255,170)
    elif int(currentTemp)<32:
        COLOR=(240,230,140)
    else:
        COLOR=(255,165,0)
    TempFont=pygame.freetype.Font('FontLib/setup/楷体.TTF',96)
    TempFont.render_to(screen,(830-330,1222+50),currentTemp+'℃',COLOR,10)

    HumidityFont=pygame.freetype.Font('FontLib/setup/楷体.TTF',20)
    HumidityFont.render_to(screen,(968-330,1133+40+50),WeatherMessage['TodayInfo']['空气湿度'],(0,0,0),10)

    SuggestionFont=pygame.freetype.Font('FontLib/setup/楷体.TTF',24)
    #UV=pygame.image.load('FunIcon/UV.png')
    #UVRect=UV.get_rect()
    #UVRect.left=590+48-330
    #UVRect.top=1165+50
    #screen.blit(UV,UVRect)
    #SuggestionFont.render_to(screen,(640+48-330,1175+50),'UV:'+SuggestionMessage['uv']['brief'],(255,255,255),10)
    #SuggestionFont.render_to(screen,(640+48-330,1175+50),'UV:'+SuggestionMessage['uv']['brief'],(255,255,255),10)

    Cloth = pygame.image.load('FunIcon/Cloth.png')
    ClothRect = Cloth.get_rect()
    ClothRect.left = 590+48-330
    ClothRect.top = 1215+50
    screen.blit(Cloth, ClothRect)
    SuggestionFont.render_to(screen, (640+48-330, 1225+50), '穿衣:' + SuggestionMessage['dressing']['brief'], (255, 255, 255), 10)

    Sport = pygame.image.load('FunIcon/sport.png')
    SportRect = Sport.get_rect()
    SportRect.left = 590+48-330
    SportRect.top = 1265+50
    screen.blit(Sport, SportRect)
    SuggestionFont.render_to(screen, (640+48-330, 1275+50), '运动:' + SuggestionMessage['sport']['brief'], (255, 255, 255), 10)

    Sick = pygame.image.load('FunIcon/sick.png')
    SickRect = Sick.get_rect()
    SickRect.left = 590+48-330
    SickRect.top = 1315+50
    screen.blit(Sick, SickRect)
    SuggestionFont.render_to(screen, (640+48-330, 1325+50), '流感' + SuggestionMessage['flu']['brief'], (255, 255, 255), 10)

def showMoreWeather():
    IntroFont = pygame.freetype.Font('FontLib/setup/楷体.TTF', 32)
    IntroFont.render_to(screen,(814-330,1380+50),"未来三日",(255,255,255),10)
    pygame.draw.line(screen,(255,255,255),(680-330-42,1418+50),(1080-330,1418+50))

    FutureFont = pygame.freetype.Font('FontLib/setup/楷体.TTF', 32)
    for i in range(3): 
        day=''
        if i==0:
            day='今天'
        if i==1:
            day='明天'
        if i==2:
            day='后天'
        FutureFont.render_to(screen,(680-330-42,1426+50+i*35),day,(255,255,255),10)
        FutureFont.render_to(screen,(830-330,1426+50+i*35),WeatherMessage['More'][i][0],(255,255,255),10)
        FutureFont.render_to(screen, (960-330, 1426+50 + i * 35), WeatherMessage['More'][i][1], (255, 255, 255), 10)

# =============================================================================
# Sentence=Fun.getSentence()
# def showSentence():
#     SentenceFont=pygame.freetype.Font("FontLib/setup/楷体.TTF",36)
#     length=len(Sentence)
#     SentenceFont.render_to(screen,(540-36*length/2,850),Sentence,(255,255,255),10)
    
History=Fun.getHistory(Time.getDate())
def showHistory():
    NameFont=pygame.freetype.Font("FontLib/setup/楷体.TTF",42)
    NameFont.render_to(screen,(50,1700),"『史·鉴』",(255,255,255),10)
    ContentFont=pygame.freetype.Font("FontLib/setup/楷体.TTF",30)
    ContentFont.render_to(screen,(50,1750),History,(255,255,255),10)

def showHello(name):
     NameFont=pygame.freetype.Font("FontLib/setup/楷体.TTF",54)
     NameFont.render_to(screen,(650,550),"Welcome  "+name,(255,255,255),10)
     #GreetingFont=pygame.freetype.Font("FontLib/setup/楷体.TTF",42)
     #GreetingFont.render_to(screen,(275,910),"Good afternoon!",(255,255,255),10)

H='H.txt'
T='T.txt'
def gethumidity():
    f=open(H,'r')
    h=f.readline()
    h=str(h)
    return h
def gettemperature():
    f=open(T,'r')
    t=f.readline()
    t=str(t)
    return t

Humidity=gethumidity()
Temperature=gettemperature()
def showH_T():
     HFont=pygame.freetype.Font("FontLib/setup/楷体.TTF",36)
     HFont.render_to(screen,(50,1050),"湿度: "+Humidity+" %",(255,255,255),10)
     TFont=pygame.freetype.Font("FontLib/setup/楷体.TTF",36)
     TFont.render_to(screen,(50,1100),"温度: "+Temperature+" ℃",(255,255,255),10)
     
# def showHello1():
#     NameFont=pygame.freetype.Font("FontLib/setup/楷体.TTF",42)
#     NameFont.render_to(screen,(275,850),"Welcome,Yan!",(255,255,255),10)
#     GreetingFont=pygame.freetype.Font("FontLib/setup/楷体.TTF",42)
#     GreetingFont.render_to(screen,(275,910),"Good afternoon!",(255,255,255),10)
    

    
#树莓派中要将show函数放入循环内部！
showHot()
# showAgenda()
showMainWeather()
showMoreWeather()
showHistory()
showH_T()
# showHello()

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    FormatDate = Time.getDate()
    #覆盖掉时钟区域
    screen.fill((0, 0, 0),rect=(0,0,1000,450))#需要实时刷新的其实就只有时间
    if Time.getMinute()%5==0 and Time.getSec()==0:#整点更新API数据
        screen.fill((0,0,0))
        History=Fun.getHistory(Time.getDate())
        currentTemp=Weather.getCurrentWeather()
        WeatherMessage=Weather.getWeather()
        SuggestionMessage =Weather.getSuggestion()
        Zhihu=topque.GetTopQue()
        Hot=Fun.getHot()
        Humudity=gethumidity()
        Temperature=gettemperature()
        showHot()
        showH_T()
        # showAgenda()
        showMainWeather()
        showMoreWeather()
        showHistory()
    # 显示的信息一旦show后，就一直在
    # 如果要更改，拿黑色背景遮盖后显示新的！！
    # if Time.getMinute()%2==0:
    #     screen.fill((0,0,0),rect=(270,840,100,80))
    #     showHello()
    # if Time.getMinute()%2!=0:
    #     screen.fill((0,0,0),rect=(270,840,100,80))
    #     showHello1()
    if GPIO.input(people)==GPIO.HIGH:
        name=agenda.Getname()
        website=agenda.GetURL(name)
        try:
            Agenda=agenda.GetAgenda(website)
            showHello(name)
            showAgenda(Agenda)
        except:
            showerr()
    else:
        screen.fill((0, 0, 0),rect=(640,500,500,425))
    showTime()
    clock.tick(FPS)
    pygame.display.update()    
    
    
    
