import pygame

class TextLabel:
	"""Simple class for dealing with labels"""

	def __init__(self, newX, newY, newText, newFontSize):
		self.xPos = newX
		self.yPos = newY
		self.text = newText
		self.fontSize = newFontSize

		if pygame.font:
			self.font = pygame.font.Font(None, self.fontSize)
        

	def draw(self, screen):
		text = self.font.render(self.text, 1, (255, 255, 255))
		textpos = text.get_rect(centerx=self.xPos, centery = self.yPos)
		screen.blit(text, textpos)
