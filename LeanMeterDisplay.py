import Utility
import pygame
import math

class LeanMeterDisplay:
	def __init__(self, gyroObj):
		self.radius = 270
		
		self.centerX = 320
		self.centerY = 440
		
		self.circleXPos = 0
		self.circleYPos = 0

		self.color = (255, 255, 255)
		self.gyroObj = gyroObj

		self.warning = False
		self.warningColor = (255, 255, 0)

	def draw(self, screen):
		Utility.drawCircleArc(screen, self.color, (self.centerX, self.centerY), self.radius + 10, 0, 181, 15)

		if self.warning:
			pygame.draw.circle(screen, self.warningColor, (int(self.circleXPos), int(self.circleYPos)), 35, 15)
		else:
			pygame.draw.circle(screen, self.color, (int(self.circleXPos), int(self.circleYPos)), 35, 15)

		pygame.draw.lines(screen, self.color, False, [(320, 150), (320, 185)], 5)
		pygame.draw.lines(screen, self.color, False, [(30, 440), (65, 440)], 5)
		pygame.draw.lines(screen, self.color, False, [(575, 440), (610, 440)], 5)

	def update(self):
		self.circleXPos = self.centerX + self.radius * math.cos(Utility.degreesToRadians(90 - self.gyroObj.roll))
		self.circleYPos = self.centerY - 1 - self.radius * math.sin(Utility.degreesToRadians(90 - self.gyroObj.roll))

		self.warning = self.gyroObj.rollChangeThresholdWarning
