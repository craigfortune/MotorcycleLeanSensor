import pygame
import math

def drawCircleArc(screen,color,center,radius,startDeg,endDeg,thickness):
    (x,y) = center
    rect = (x-radius,y-radius,radius*2,radius*2)
    startRad = degreesToRadians(startDeg)
    endRad = degreesToRadians(endDeg)
   
    pygame.draw.arc(screen,color,rect,startRad,endRad,thickness)

def degreesToRadians(deg):
    return deg/180.0 * math.pi