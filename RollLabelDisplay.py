import TextLabel

class RollLabelDisplay:

	def __init__(self, gyroObj):
		self.gyroObj = gyroObj
		self.maxLeanLabel = TextLabel.TextLabel(320, 330, "00", 285)
		self.leftLeanLabel = TextLabel.TextLabel(85, 60, "L --", 85)
		self.rightLeanLabel = TextLabel.TextLabel(535, 60, "R 24", 85)

	def update(self):
		if self.gyroObj.roll > 90:
			self.gyroObj.roll = 90

		if self.gyroObj.roll < -90:
			self.gyroObj.roll = -90

		if self.gyroObj.greatestVal < 10 and self.gyroObj.greatestVal > -10:
			self.maxLeanLabel.text = "0" + str(self.gyroObj.greatestVal)
		else:
			self.maxLeanLabel.text = str(self.gyroObj.greatestVal)

		# Side labels
		if self.gyroObj.roll < 0:
			self.leftLeanLabel.text = "L" + str(int(abs(self.gyroObj.roll)))
			self.rightLeanLabel.text = "R --"
		elif self.gyroObj.roll > 0:
			self.leftLeanLabel.text = "L --"
			self.rightLeanLabel.text = "R" + str(int(abs(self.gyroObj.roll)))
		else:
			self.leftLeanLabel.text = "L --"
			self.rightLeanLabel.text = "R --"

	def draw(self, screen):
		self.leftLeanLabel.draw(screen)
		self.rightLeanLabel.draw(screen)
		self.maxLeanLabel.draw(screen)