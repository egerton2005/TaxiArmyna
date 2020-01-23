#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

# CONST
leftMotor = Motor(Port.A)
rightMotor = Motor(Port.B)
captureMotor = Motor(Port.C)
scrollingMotor = Motor(Port.D)
colorSensor = ColorSensor(Port.S2)
colorSensorRight = ColorSensor(Port.S4)
colorSensorLeft = ColorSensor(Port.S3)
Const_povovorot = 170
Const_reflection_limit = 10
Const_speed_fline = 150
Const_slow_speed_fline = 50
location = [False,False,False,False,False,False]
gyroSensor = GyroSensor(Port.S1)


def gyroSensorIsTrue():
    angle = gyroSensor.angle() % 360
    return (angle < 80 or angle > 110)

#поворот на 90 градусов
#angle - угол(градусов)
def povorot(angle):
    leftMotor.reset_angle(0)
    leftMotor.dc(50)
    rightMotor.dc(-50)
    print('povorot:'+angle)
    while(abs(leftMotor.angle()) < angle):
        leftMotor.stop
        rightMotor.stop

#ехать вперёд
#left,right моторы
def motorRule(left,right):
    leftMotor.run(left)
    rightMotor.run(right)

#езда по черной линии
#crossroadCounts - кол-во перекрестков, которые необходимо проехать
def crossroad (crossroadCounts):
    print('crossroad:'+crossroadCounts)
    crossroad = 0
    blackLine = False
    while(True):
        reflectionLEFT = colorSensorLeft.reflection()
        reflectionRight = colorSensorRight.reflection()

        fline(reflectionLEFT, reflectionRight)
        
        if((reflectionLEFT < Const_reflection_limit) & (reflectionRight < Const_reflection_limit)):
            if(blackLine == False):
                crossroad = crossroad + 1
            
            blackLine = True
        else:
            blackLine = False
            if(crossroad == crossroadCounts):
                motorRule(0,0)
                break


#readingОbstacles считывание препятствий
#obstacleCounts кол-во препятствий 
def readingОbstacles (obstacleCounts):
    print('readingОbstacles:'+str(obstacleCounts))
    obstacle = 0   
    readingОbstacles = False
    while(True):
        reflectionLEFT = colorSensorLeft.reflection()
        reflectionRight = colorSensorRight.reflection()

        fline(reflectionLEFT, reflectionRight)

        print(gyroSensorIsTrue())
        if (colorSensor.color() != None and gyroSensorIsTrue()):
            if(readingОbstacles == False):
                obstacle = obstacle + 1
            readingОbstacles = True

            if(obstacle >= obstacleCounts):
                break
        else:
            readingОbstacles == False

def fline(reflectionLEFT, reflectionRight):
    if(reflectionLEFT < Const_reflection_limit):
        if(reflectionRight < Const_reflection_limit):
            motorRule(Const_speed_fline,Const_speed_fline)
        else:
            motorRule(-Const_slow_speed_fline,Const_slow_speed_fline)
    else:
        if(reflectionRight < Const_reflection_limit):
            motorRule(Const_slow_speed_fline,-Const_slow_speed_fline)
        else:
            motorRule(Const_speed_fline,Const_speed_fline)


def thisColor():
    if colorSensor.color() != None:
        color = colorSensor.color()
    else:
        print('не увидел цвет')
    return color

def distributor():
    step = 0
    while(0<6):
        readingОbstacles(1) #Проехал до кубика
        colorFirst = thisColor() #считал цвет кубика
        print('colorFirst:'+str(colorFirst))
        print('Взял:')

        #прокрутка вниз
        #взять
        #прокрутка вверх
        readingОbstacles(5 - step + 1)
        for x in range(0,6):
            colorSecond = thisColor()
            print('colorSecond:'+colorSecond)
            if(colorFirst==colorSecond & location[x] == False):
                #прокрутка вниз
                #поставить
                #прокрутка вверх
                location[x] == True
                print('Поставил:')
                readingОbstacles(5 - x)
                step = step + 1
                break
            else:
                readingОbstacles(1)




gyroSensor.reset_angle(0)
distributor()