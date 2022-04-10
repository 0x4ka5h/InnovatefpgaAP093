import time
import cv2
import numpy
import requestFunction
import threading
import gpiopy
import controllingByRemote

time.sleep(5)
#cap = cv2.VideoCapture("http://192.168.42.129:4747/video")


faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
C_=1
K_=1

def intializingPins():
	## for switch connection
	gpiopy.gpioExport(1803)
	gpiopy.gpioExport(1804)
	gpiopy.gpioDirec(1803,"out")
	gpiopy.gpioValue(1803,1)
	gpiopy.gpioDirec(1804,"in")
	## for leds
	gpiopy.gpioExport(1805)   ## for green led
	gpiopy.gpioExport(1806)   ## for red led
	gpiopy.gpioDirec(1805,"out")
	gpiopy.gpioValue(1805,0)
	gpiopy.gpioDirec(1806,"out")
	gpiopy.gpioValue(1806,1)
	

def alterRedLed():
	val = 0
	while C_:
		try:
			if val==0:
				val = 1
				#print("redlight on")
			else:
				val = 0
			gpiopy.gpioValue(1822,val)
		except:
			print("Exception at alterRedLED")
		

def switchTrigger():
	while K_:
		try:
			val = gpiopy.gpioRead(1804)
			if int(str(val[0])) == 1:
				ownerCheck()
				break
		except:
			print("Exception at switchTrigger")


def ownerCheck():
	face = True
	tries = 0
	while face or tries>2:
		#_,grayImage = cap.read()
		grayImage = cv2.imread("g00g1y5p4.jpg",2)
		print(grayImage)
		response = requestFunction.ownerFriendValidation(grayImage)
		print(response)
		print(type(response))
		try:
			response = response.decode('utf-8')
		except:
			pass
		if (response=="1"):
			## engine starts
			gpiopy.gpioValue(1805,1)
			C_=0
			return
		elif (response=="0"):
			## block engine
			C_=0
			#print()
			gpiopy.gpioValue(1805,0)
			
			return
		else:
			data = requestFunction.checkAcceptance()
			if data['allow']==1:
				## engine starts
				C_=0
				gpiopy.gpioValue(1805,1)
				
				return
			else:
				## block engine
				C_=0
				gpiopy.gpioValue(1805,0)
				return
	else:
		## engine starts
		gpiopy.gpioValue(1821,1)
		
intializingPins()
ownerCheck()

