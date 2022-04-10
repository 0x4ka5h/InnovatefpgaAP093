import time
import cv2
import numpy
import requestFunction
import threading
import gpiopy

#cap = cv2.VideoCapture("http://192.168.42.129:4747/video")

def controlMotors():
	while True:
		controlData = requestFunction.remoteCommandsToVehicle()
		# {'acccelarationFunc_': 0, 'breakFunc_': 0, 'steerAngle_': -11}
		if controlData['breakFunc_'] == 1:
			#stop motors 
		 	gpiopy.gpioDirec(1805,"in")
		 	gpiopy.gpioDirec(1806,"in")
		 	pass
		elif controlData['acccelarationFunc_'] == 1:
		 	#release motors
		 	gpiopy.gpioDirec(1805,"out")
		 	gpiopy.gpioDirec(1806,"out")
		 	gpiopy.gpioValue(1805,1)
		 	gpiopy.gpioValue(1806,1)
		 	pass

def sendCamImage():
	while True:
		#_,img = cap.read()
		img = cv2.imread("dp1.png",2)
		requestFunction.camStream(2,img)

t=threading.Thread(target=controlMotors)
t.start()

t1=threading.Thread(target=sendCamImage)
t1.start()

