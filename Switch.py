import RPi.GPIO as GPIO

class Switch:

	def __init__(self, inChannel):
		self.inChannel = inChannel
		self.lastSwitchState = 0
		self.switchState = False
		self.debugText = False

		# Simple setup
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(inChannel, GPIO.IN)

	def update(self):
		self.switchState = False
		currSwitchState = GPIO.input(self.inChannel)

		if self.lastSwitchState == 1 and currSwitchState == 0:
			self.switchState = True
			if self.debugText:
				print "Switch pressed!"

		self.lastSwitchState = currSwitchState