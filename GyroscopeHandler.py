import time
from operator import attrgetter

import GyroscopeHardware
import GyroAxisData

class GyroscopeHandler:

	def __init__(self, switch, deltaThreshold, selfCorrectingThreshold):
		self.gyroscopeHardware = GyroscopeHardware.GyroscopeHardware()
		self.switch = switch

		self.rollOffset = 0
		self.pitchOffset = 0
		self.yawOffset = 0

		self.roll = 0;
		self.pitch = 0;
		self.yaw = 0;

		self.rollBuffer = []
		self.pitchBuffer = []
		self.yawBuffer = []

		self.greatestVal = 0
		self.maxLeanTimeout = 5000

		self.rollChangeThresholdWarning = False

		self.deltaThreshold = deltaThreshold
		self.selfCorrectingThreshold = selfCorrectingThreshold


	def update(self):
		self.gyroscopeHardware.update()
		self.grabGyroVals()

		if self.switch.switchState:
			print "Gyroscope logging current offset values as origin"
			self.setCurrentStateAsOffsets()

		# Store the highest roll value from the last X seconds
		rollDataObj = GyroAxisData.GyroAxisData("roll", abs(self.roll), int(round(time.time() * 1000)))
		self.rollBuffer.append(rollDataObj)

		while True:
			if int(round(time.time() * 1000)) - self.rollBuffer[0].time > self.maxLeanTimeout:
				self.rollBuffer.pop(0)
			else:
				break

		self.greatestVal = max(self.rollBuffer, key=attrgetter("val")).val

	def setCurrentStateAsOffsets(self):
		self.setGyroOffsets(self.roll, self.pitch, self.yaw)

	def validateNewValue(self, errorStr, gyroAttribStr, thisAttribStr, deltaThreshold, selfCorrectingThreshold):
		gyroAttribVal = getattr(self.gyroscopeHardware, gyroAttribStr)
		thisAttribVal = getattr(self, thisAttribStr)

		if abs(gyroAttribVal - thisAttribVal) < deltaThreshold:
			setattr(self, thisAttribStr, int(gyroAttribVal))
		elif abs(gyroAttribVal) < selfCorrectingThreshold:
			setattr(self, thisAttribStr, int(gyroAttribVal))
		else:
			print errorStr + "\t" + str(abs(gyroAttribVal - thisAttribVal))
			return False

		# Default case
		return True

	def setGyroOffsets(self, roll, pitch, yaw):
		self.rollOffset = roll
		self.pitchOffset = pitch
		self.yawOffset = yaw

		print "Offsets:"
		print 'Roll: {} Pitch: {} Yaw: {}'.format(self.rollOffset, self.pitchOffset, self.yawOffset)

	def grabGyroVals(self):
		if not self.validateNewValue("REFUSING ROLL", "roll", "roll", self.deltaThreshold, self.selfCorrectingThreshold):
			self.rollChangeThresholdWarning = True
		else:
			self.rollChangeThresholdWarning = False

		self.validateNewValue("REFUSING PITCH", "pitch", "pitch", self.deltaThreshold, self.selfCorrectingThreshold)
		self.validateNewValue("REFUSING YAW", "yaw", "yaw", self.deltaThreshold, self.selfCorrectingThreshold)
