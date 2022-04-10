import requests
import cv2
import numpy as np
from PIL import Image
import base64
import io

sessionId_ = requests.Session()

url = "http://192.168.137.149:5000"
global finalImage
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


def vehicleStatus():
	req = sessionId_.get(url+"/api/vehicleStatus")

	if (req.json()['status']):
		return req.json()['status']
	else:
		return "301"


###################################################     '''''''      GPS      ''''''''''         ################################

def gpsLocation(code):
	data = {"vehicleCode":code}
	req = sessionId_.post(url+"/api/gpsLocationCurrent/",json = data)


	if (req.status_code == 201):
		return req.json()['gpsLocation']
	else:
		return "0"


def gpsTracker(code):
	data = {"vehicleCode":code}
	req = sessionId_.post(url+"/api/gpsLocationTrack/",json = data)


	if (req.status_code == 201):
		return req.json()
	else:
		return "0"

def gpsCoveredPaths(code):
	data = {"vehicleCode":code}
	req = sessionId_.post(url+"/api/gpsLocationCovered/",json = data)


	if (req.status_code == 201):
		return req.json()
	else:
		return "0"

#####################################     '''''''      Driving Mode and Camera View     ''''''''''         ################################
def drivingModes(mode,view):
	data = {'mode':mode,'view':view}		# 0-Normal , 1-Remote mode , 2-AutoMode # 0-off , 1-inside camera view , 2-outsideView
	req = sessionId_.post(url+"/api/commands/commandsPassing/",json = data)

'''#############    '''''''       Remote Driving Mode      ''''''''''        #############'''


def remoteCommandsToVehicle(angle_,break_,accelarator_):
	data = {'steerAngle':angle_,'breakFunc':break_,'acccelarationFunc':accelarator_}
	req = sessionId_.post(url+"/api/fromOwner/forRemote/remoteCommandsToVehicle/",json = data)

def retrieveforRC():
	req = sessionId_.get(url+"/api/fromVehicle/forRemote/retrieveforRC/")
	if (req.status_code == 201):
		speed_ = req.json()['speed_']
		usLeft_ = req.json()['ultraSonicLeft_']
		usBack1_ = req.json()['ultraSonicBack1_']
		usRight_ = req.json()['ultraSonicRight_']
		return speed_,usLeft_,usRight_,usBack1_
	else:
		return "0"

def camViewByIndex(index):
	data = {'camIndex':index}
	req = sessionId_.post(url+"/api/stream/cameraStreamByOwner/",json=data)
	try:
		if (req.status_code == 200):
			dec = base64.b64decode(req.content)
			nparr = np.fromstring(dec, np.uint8)
			image_ = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
			#image_ = cv2.rotate(image_,cv2.ROTATE_90_COUNTERCLOCKWISE)
			pilImage = Image.fromarray(image_)

			byteIO = io.BytesIO()
			pilImage.save(byteIO,format='PNG')
			finalImage = base64.b64encode(byteIO.getvalue())
			return ""+ str(finalImage,'utf-8')
		else:
			return "0"
	except:
		return ""+ str(finalImage,'utf-8')

def validateThroughNotification(index):
	req = sessionId_.get(url+"/api/vehicle/validateThroughNotification/")
	if (req.status_code == 200):
		if index==0:
			return req.json()['isUnknown']
		elif index==1:
			return req.json()['isTowing']
		elif index==2:
			return req.json()['isDeclined']
	else:
		return "0"

def acceptORdecline(choice):
	data = {'choice':choice}
	sessionId_.get(url+"/api/vehicle/AcceptanceORDecline/",json = data)


def autoMode(gps="0"):
	if gps=="0":
		sessionId_.post(url+"/api/sendautoInstruction/",json={'gps':"0",'pPath':1})
	else:
		sessionId_.post(url+"/api/sendautoInstruction/",json={'gps':str(gps),'pPath':0})
	return "1"