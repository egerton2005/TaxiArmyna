#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
import time

# Motor
leftMotor = Motor(Port.A)
rightMotor = Motor(Port.B)
captureMotor = Motor(Port.C)
scrollingMotor = Motor(Port.D)
# Sensor
colorSensor = ColorSensor(Port.S2)
colorSensorRight = ColorSensor(Port.S4)
colorSensorLeft = ColorSensor(Port.S3)
gyroSensor = GyroSensor(Port.S1)
# CONST
Const_povovorot = 200
Const_reflection_limit = 10
Const_speed_fline = 150
Const_slow_speed_fline = 50
Const_speed_motors = 50
Const_speed_goforward = 100

location = [False,False,False,False,False,False]

#измеряет угол поворота относительно начала и если робот находится в промежутке между 
# 80 и 110 градусами то метод выдаёт ложь
def gyroSensorIsTrue():
    angle = gyroSensor.angle() % 360
    return (angle < 80 or angle > 110)
    
#povorot поворачивает двумя моторами
#angle - данные об угле поворота моторов
def povorot(angle):
    leftMotor.reset_angle(0)
    if(angle<0):
        motorRule(-Const_speed_motors, Const_speed_motors)
    else:
        motorRule(Const_speed_motors, -Const_speed_motors)
    print('povorot:'+str(angle))
    while(True):
        if abs(leftMotor.angle()) >= abs(angle):
            break

    motorsStop()

#езда прямо, запускающая сразу 2 мотора
#left,right скорость левого и правого моторов
def motorRule(left,right):
    leftMotor.run(left)
    rightMotor.run(right)

# запускаем оба мотора одновременно, на определённое время
# left,right скорость двух моторов
# times время пути
def goforward(left,right,times):
    print("проехать вперёд:" + str(time))
    motorRule(left, right)
    print("записываем время")
    oldTime = time.time()
    print("записываем время второй раз")
    print("находим разность нового и старого времени и сравниваем с заданым временем")
    while(True):
        newTime = time.time()
        if(newTime - oldTime >=times):
            break

# bucket запускает ковш для захвата кубика
# speed,times задаваемое время и скорость
def bucket(speed,times):
    captureMotor.run(speed)
    oldTime = time.time()
    while(True):
        newTime = time.time()
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
                motorsStop()
                break

#оба мотора останавливаются 
def motorsStop():
    leftMotor.stop()
    rightMotor.stop()

#readingОbstacles считывание препятствий
#obstacleCounts кол-во препятствий 
def readingОbstacles (obstacleCounts):
    print('readingОbstacles:'+str(obstacleCounts))
    obstacle = 0   
    readingОbstacles = False
    iteration = 0
    while(True):
        if(iteration % 3 == 0):
            reflectionLEFT = colorSensorLeft.reflection()
            reflectionRight = colorSensorRight.reflection()
            print("сравниваем значения")
            fline(reflectionLEFT, reflectionRight)

        if (colorSensor.color() != None and gyroSensorIsTrue()):
            if(readingОbstacles == False):
                brick.sound.beeps(5)
                print("увидел новое препядствие")
                obstacle = obstacle + 1
            readingОbstacles = True
            if(obstacle >= obstacleCounts):
                print("остоновился")
                break
        else:
            readingОbstacles == False
        iteration = iteration + 1

#езда по чёрной линии
#reflectionLEFT, reflectionRight степень отражённости света (для езды по чёрной линии)
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

#считывает цвет и возвращает его
def thisColor():
    if colorSensor.color() != None:
        color = colorSensor.color()
        print("color")
    else:
        print('не увидел цвет')
    return

def findColor():
    while(True):
        colorSensor.color()  
        print(colorSensor.color())

#распределяет цвет кубика на цвет целиндра 
def distributor():
    for step in range(0,6):
        readingОbstacles(1) #Проехал до кубика
        print("distributor:" + str(readingОbstacles))
        colorFirst = thisColor() #считал цвет кубика
        print('colorFirst:'+str(colorFirst))
        motorsStop()
        print("опустил ковш")
        bucket(-Const_speed_goforward, 1.5)
        print("поднял ковш")
        readingОbstacles(5 - step + 1)
        for x in range(0,6):
            colorSecond = thisColor()
            print('colorSecond:'+ str(colorSecond))
            if(colorFirst==colorSecond & location[x] == False):
                print("сравнил")
                location[x] == True
                bucket(Const_speed_goforward, 1.5)
                print('Поставил:')
                readingОbstacles(5 - x)
                print("readingОbstacles:" + str(step))
                break
            else:
                readingОbstacles(1)
                print("повторяем")


gyroSensor.reset_angle(0)
goforward(Const_speed_goforward, Const_speed_goforward, 1.5)
crossroad(1)
povorot(-Const_povovorot)
distributor()