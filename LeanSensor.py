#! /usr/bin/env python

import os, sys

import pygame
from pygame.locals import *

import math
import time

import GyroscopeHandler
import GyroscopeHardware
import GyroAxisData
import TextLabel
import Utility
import LeanMeterDisplay
import FPSLabel
import RollLabelDisplay

import Switch

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

roll = 0

class PyManMain:
    """The Main PyMan Class - This class handles the main 
    initialization and creating of the Game."""

    def __init__(self, width=640,height=480):

        #Initialize PyGame
        pygame.init()
        pygame.mouse.set_visible(False)
        self.setupScreen(width, height)

        self.renderList = []
        self.updateList = []

        self.switch = Switch.Switch(18)
        self.addToUpdateList(self.switch)


        self.setupGyroscope()
        self.setupLabels()
        self.setupLeanMeterDisplay()

    def setupScreen(self, width, height):
        #Set the window Size
        self.width = width
        self.height = height
        
        #Create the Screen
        self.screen = pygame.display.set_mode((self.width, self.height))        
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((205, 50, 50))
        
    def setupGyroscope(self):
        self.gyroscopeHandler = GyroscopeHandler.GyroscopeHandler(self.switch, 15, 10)
        self.addToUpdateList(self.gyroscopeHandler)

    def setupLeanMeterDisplay(self):
        self.leanMeterDisplay = LeanMeterDisplay.LeanMeterDisplay(self.gyroscopeHandler)
        self.addToUpdateAndRenderList(self.leanMeterDisplay)

    def setupLabels(self):
        self.FPSLabel = FPSLabel.FPSLabel()
        self.addToUpdateAndRenderList(self.FPSLabel)

        self.rollLabelDisplay = RollLabelDisplay.RollLabelDisplay(self.gyroscopeHandler)
        self.addToUpdateAndRenderList(self.rollLabelDisplay)

    def addToRenderList(self, objectToAdd):
        self.renderList.append(objectToAdd)

    def addToUpdateList(self, objectToAdd):
        self.updateList.append(objectToAdd)

    def addToUpdateAndRenderList(self, objectToAdd):
        self.addToUpdateList(objectToAdd)
        self.addToRenderList(objectToAdd)

    def updateScene(self):
        for i in range(0, len(self.updateList)):
            self.updateList[i].update()

    def drawScene(self):
        self.screen.blit(self.background, (0, 0))
        
        for i in range(0, len(self.renderList)):
            self.renderList[i].draw(self.screen)

        pygame.display.update()

    def MainLoop(self):        
        while 1:

            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()

                if event.type == KEYDOWN:
                    pygame.quit()
                    return

            self.updateScene()
            self.drawScene()


# Load everything up if this is the main script

if __name__ == "__main__":
    MainWindow = PyManMain()
    MainWindow.MainLoop()

