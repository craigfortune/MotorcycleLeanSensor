import time
import math
import mpu6050
import GyroAxisData

class GyroscopeHardware:

	def __init__(self):

		# Sensor initialization
		self.mpu = mpu6050.MPU6050()
		self.mpu.dmpInitialize()
		self.mpu.setDMPEnabled(True)

		# get expected DMP packet size for later comparison
		self.packetSize = self.mpu.dmpGetFIFOPacketSize()

		self.yaw = 0
		self.pitch = 0
		self.roll = 0

	def update(self):
	    # Get INT_STATUS byte
	    mpuIntStatus = self.mpu.getIntStatus()
	  
	  	# check for DMP data ready interrupt (this should happen frequently) 
	    if mpuIntStatus >= 2: 
	    
	        # get current FIFO count
	        self.fifoCount = self.mpu.getFIFOCount()
	        
	        # check for overflow (this should never happen unless our code is too inefficient)
	        if self.fifoCount == 1024:
	            # reset so we can continue cleanly
	            self.mpu.resetFIFO()
	            print('FIFO overflow!')	            
	            
	        # wait for correct available data length, should be a VERY short wait
	        self.fifoCount = self.mpu.getFIFOCount()
	        while self.fifoCount < self.packetSize:
	            self.fifoCount = self.mpu.getFIFOCount()
	        
	        result = self.mpu.getFIFOBytes(self.packetSize)
	        q = self.mpu.dmpGetQuaternion(result)
	        g = self.mpu.dmpGetGravity(q)
	        ypr = self.mpu.dmpGetYawPitchRoll(q, g)

	        self.yaw = ypr['yaw'] * 180 / math.pi
	        self.pitch = ypr['pitch'] * 180 / math.pi
	        self.roll = ypr['roll'] * 180 / math.pi
	    
	        # track FIFO count here in case there is > 1 packet available
	        # (this lets us immediately read more without waiting for an interrupt)        
	        self.fifoCount -= self.packetSize

			# CRAIG
	        # Clear the FIFO buffer else it'll overflow!
	        self.mpu.resetFIFO()

	def display(self):
		print "Yaw: " + str(self.yaw) + "\t Pitch: " + str(self.pitch) + "\t Roll: " + str(self.roll)

if __name__ == "__main__":
	
	gyroDataObject = GyroData()

	while True:
		gyroDataObject.update()
		gyroDataObject.display()
		time.sleep(0.1)