#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

# Write your program here
brick.sound.beep()
leftMotor = Motor(Port.A)
rightMotor = Motor(Port.B)
captureMotor = Motor(Port.C)
scrollingMotor = Motor(Port.D)
colorSensor = ColorSensor(Port.S2)
colorSensorRight = ColorSensor(Port.S4)
colorSensorLeft = ColorSensor(Port.S3)
haight = UltrasonicSensor(Port.S2)
Const_povovorot = 170
REFLECTION_LIMIT = 10
SPEED_FLINE = 150
SLOW_SPEED_FLINE = 50
Color.BLACK = 1
Color.BLUE = 2
Color.GREEN = 3
Color.YELLOW = 4
Color.RED = 5
Color.WHITE = 6
Color.BROWN = 7
location = [
False,False,False,False,False,False
]


def povorot(angle):
    leftMotor.reset_angle(0)
    leftMotor.dc(50)
    rightMotor.dc(-50)
    while(abs(leftMotor.angle()) < angle):
        print(abs(leftMotor.angle()))
        leftMotor.stop
        rightMotor.stop


def motorRule(left,right):
    motorLeft.run(left)
    motorRight.run(right)

#езда по черной линии
#crossroadCounts - кол-во перекрестков, которые необходимо проехать
def crossroad (crossroadCounts):
    crossroad = 0
    blackLine = False
    while(True):
        reflectionLEFT = colorSensorLeft.reflection()
        reflectionRight = colorSensorRight.reflection()

        fline(reflectionLEFT, reflectionRight)
        
        if((reflectionLEFT < REFLECTION_LIMIT) & (reflectionRight < REFLECTION_LIMIT)):
            if(blackLine == False):
                crossroad = crossroad + 1
            if(crossroad == crossroadCounts):
                motorRule(0,0)
                break
            blackLine = True
        else:
            blackLine = False



def readingОbstacles (obstacleCounts):
    obstacle = 0   
    readingОbstacles = False
    while(True):
        reflectionLEFT = colorSensorLeft.reflection()
        reflectionRight = colorSensorRight.reflection()

        fline(reflectionLEFT, reflectionRight)
        
        if (colorSensor != None):
            if(readingОbstacles == False)
                obstacle = obstacle + 1
            readingОbstacles = True
        else:
            readingОbstacles == False
        if(obstacle >= obstacleCounts):
            break

def fline(reflectionLEFT, reflectionRight):
    if(reflectionLEFT < REFLECTION_LIMIT):
            if(reflectionRight < REFLECTION_LIMIT):
                motorRule(SPEED_FLINE,SPEED_FLINE)
            else:
                motorRule(-SLOW_SPEED_FLINE,SLOW_SPEED_FLINE)
        else:
            if(reflectionRight < REFLECTION_LIMIT):
                motorRule(SLOW_SPEED_FLINE,-SLOW_SPEED_FLINE)
            else:
                motorRule(SPEED_FLINE,SPEED_FLINE)


def thisColor(colorSensor):
    if colorSensor.Color() != None:
        color = colorSensor.Color()
    return color

def distributor():
    step = 0
    while(0<6):
        readingОbstacles(1)#Проехал до кубика
        colorFirst = thisColor()#считал цвет кубика
        #прокрутка вниз
        #взять
        #прокрутка вверх
        readingОbstacles(5 - step + 1)
        for( x in range(0,6)):
            colorSecond = thisColor()
            if(colorFirst==colorSecond & location[x] == False):
                #прокрутка вниз
                #поставить
                #прокрутка вверх
                location[x] == True
                readingОbstacles(5 - x)
                break
            else:
                readingОbstacles(1)
            



