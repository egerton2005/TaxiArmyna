#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
import time

# CONST
leftMotor = Motor(Port.A)
rightMotor = Motor(Port.B)
captureMotor = Motor(Port.C)
scrollingMotor = Motor(Port.D)
colorSensor = ColorSensor(Port.S2)
colorSensorRight = ColorSensor(Port.S4)
colorSensorLeft = ColorSensor(Port.S3)
gyroSensor = GyroSensor(Port.S1)
Const_povovorot = 200
Const_reflection_limit = 10
Const_speed_fline = 150
Const_slow_speed_fline = 50
location = [False,False,False,False,False,False]

#измеряет угол поворота относительно начала и если робот находится в промежутке между 
# 80 и 110 градусами то метод выдаёт ложь
def gyroSensorIsTrue():
    angle = gyroSensor.angle() % 360
    return (angle < 80 or angle > 110)
    
#povorot поворачивает двумя моторами на 90 градусов
#angle - данные об угле поворота моторов
def povorot(angle):
    leftMotor.reset_angle(0)
    if(angle<0):
        leftMotor.dc(-50)
        rightMotor.dc(50)
    else:
        leftMotor.dc(50)
        rightMotor.dc(-50)
    print('povorot:'+str(angle))
    while(abs(leftMotor.angle()) < abs(angle)):
        leftMotor.stop
        rightMotor.stop

#ехать вперёд
#left,right значения левого и правого моторов
def motorRule(left,right):
    leftMotor.run(left)
    rightMotor.run(right)

# запускаем оба мотора одновременно, на определённое время
def goforward(left,right,times):
    print("проехать вперёд:" + str(time))
    leftMotor.run(left)
    rightMotor.run(right)
    print("записываем время")
    oldTime = time.time()
    while(True):
        print("записываем время второй раз")
        newTime = time.time()
        print("находим разность нового и старого времени и сравниваем с заданым временем")
        if(newTime - oldTime >=times):
            break
        
#езда по черной линии
#crossroadCounts - кол-во перекрестков, которые необходимо проехать
#комментарии в самом методе
def crossroad (crossroadCounts):
    print('crossroad:'+str(crossroadCounts))
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
#комментарии в самом методе
def readingОbstacles (obstacleCounts):
    print('readingОbstacles:'+str(obstacleCounts))
    obstacle = 0   
    readingОbstacles = False
    while(True):
        reflectionLEFT = colorSensorLeft.reflection()
        reflectionRight = colorSensorRight.reflection()

        fline(reflectionLEFT, reflectionRight)

        if (colorSensor.color() != None and gyroSensorIsTrue()):
            if(readingОbstacles == False):
                print("увидел новое препядствие")
                obstacle = obstacle + 1
            readingОbstacles = True
            if(obstacle >= obstacleCounts):
                print("остоновился")
                break
        else:
            readingОbstacles == False

#TODO add coment
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


#TODO add coment
def thisColor():
    if colorSensor.color() != None:
        color = colorSensor.color()
    else:
        print('не увидел цвет')
    return color


#TODO add coment
def distributor():
    step = 0
    while(0<6):
        readingОbstacles(1) #Проехал до кубика
        print("distributor:" + str(readingОbstacles))
        colorFirst = thisColor() #считал цвет кубика
        print('colorFirst:'+str(colorFirst))
        print("опустил ковш")
        print('Взял:')
        print("поднял ковш")
        readingОbstacles(5 - step + 1)
        for x in range(0,6):
            colorSecond = thisColor()
            print('colorSecond:'+ str(colorSecond))
            if(colorFirst==colorSecond & location[x] == False):
                print("сравнил")
                location[x] == True
                print('Поставил:')
                readingОbstacles(5 - x)
                step = step + 1
                print("readingОbstacles:" + str(step))
                break
            else:
                readingОbstacles(1)
                print("повторяем")




gyroSensor.reset_angle(0)
goforward(100,100,1)
crossroad(1)
povorot(-Const_povovorot)
distributor()

