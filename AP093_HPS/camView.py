import requests
import cv2
import numpy
import requestFunctions

cap = cv2.VideoCapture("http://192.168.42.129:4747/video")

def ownerCheck():

	_,capturedFrame = cap.read()
	grayImage = cv2.imread(capturedFrame,2)
	
	
	response = ownerFriendValidation(grayImage)
	if (response=="1"):
		## engine starts
		pass
	elif (response=="0"):
		##block engine
		pass
	else:
		data = checkAcceptance()
		if data['allow']==1:
			##engine starts
			pass
		else:
			##block engine
			pass


