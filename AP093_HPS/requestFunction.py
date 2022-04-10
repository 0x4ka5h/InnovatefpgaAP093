import requests
import cv2
import numpy as np
#from PIL import Image
import base64
import io
import datetime

sessionId_ = requests.Session()

url = "http://10.4.44.130:5001"
global finalImage
#################################################### 
def convertImagetoBytes(image):
	_,encoded = cv2.imencode('.png',image)
	en = base64.b64encode(encoded)
	en = en.decode('utf-8')
	return en


###################################################     '''''''      auth      ''''''''''         ################################
def ownerSignUp(usrName,passWd_):
	data = {"type_":"owner","username":usrName,"password":passWd_}
	req = sessionId_.post(url+"/signup/",json = data)
	if (req.json()['request']=='success'):
		return "201"
	else:
		return req.json()['Reason']

def ownerLogIn(usrName,passWd_):
	data = {"type_":"owner","username":usrName,"password":passWd_}
	req = sessionId_.post(url+"/Login/",json = data)
	if (req.json()['request']=='success'):
		return "201"
	else:
		return req.json()['Reason']

def ownerLogout():
	req = sessionId_.get(url+"/logout/")


def sendVehicleDetails(usrName,driver,gps,mode):
	try:
		status_ = "Active"
		timeStamp_ = datetime.datetime.now()
		details = {'vehicleCode': usrName,'status' : status_,'timeStamp':str(timeStamp_),'driver': driver,'mode': mode,'gpsPoint': gps}
		req = sessionId_.post(url+"/api/vehicle/sendVehicleDetails/",json=details)
		return req.content
	except:
		return 

#####################################          switching Modes       ##############################

def retrieveOwnerCommands():
	try:
		req = sessionId_.get(url+'/api/commands/retrieveOwnerCommands/')
		return req.content
	except:
		return


####################################              for Remote            ############################

def parameterForRC(speed_,usLeft_,usRight_,usBack_):
	rcParameters = {'speed':speed_,'usLeft': usLeft_,'usRight' : usRight_,'usBack': usBack_ }
	try:
		req = sessionId_.post(url+"/api/fromVehicle/forRemote/parameterForRC/",json=rcParameters)
		return req.content
	except:
		return

def remoteCommandsToVehicle():
	try:
		req = sessionId_.get(url+'/api/fromOwner/forRemote/retrieveRemoteCommands/')
		return req.json()
	except:
		return
		
##########################################        for Auto        ##########################

def requestautoInstruction():
	try:
		req = sessionId_.get(url+'/api/requestautoInstruction/')
		return req.content
	except:
		return

##########################################      Camera Stream     ##############################
def camStream(index,en):
	try:
		en = convertImagetoBytes(en)
		r = sessionId_.post(url+'/api/stream/cameraStreamFromVehicle/',json={'camIndex':index,'imageData':en})
		return r.content
	except:
		return


#########################################       for faceValidation    ####################################
def ownerFriendValidation(image):
	try:
		en = convertImagetoBytes(image)
		r = sessionId_.post(url+'/api/vehicle/ownerFriendValidation/',json={'validationImage':en})
		return r.content
	except:
		return
def checkAcceptance():
	try:
		r = sessionId_.get(url+'/api/vehicle/checkAcceptance/')
		return r.json()
	except:
		return
