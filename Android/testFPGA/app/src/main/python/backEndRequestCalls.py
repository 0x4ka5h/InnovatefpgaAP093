import requests
import cv2
import numpy as np
from PIL import Image
import base64
import io

global sessionId_
sessionId_ = requests.Session()



###################################################     '''''''      auth      ''''''''''         ################################
def ownerSignUp(usrName,passWd_):
	data = {"type_":"owner","username":usrName,"password":passWd_}
	req = sessionId_.post("http://192.168.43.217:5000/signup/",json = data)

	if (req.json()['request']=='success'):
		return "201"
	else:
		return req.json()['Reason']

def ownerLogIn(usrName,passWd_):
    data = {"type_":"owner","username":usrName,"password":passWd_}
    req = sessionId_.post("http://192.168.43.217:5000/Login/",json = data)
    if (req.json()['request']=='success'):
        return "201"
    else:
        return req.json()['Reason']

def ownerLogout():
	req = sessionId_.get("http://192.168.43.217:5000/logout/")


def vehicleStatus():
	req = sessionId_.get("http://192.168.43.217:5000/api/vehicleStatus")

	if (req.json()['status']):
		return req.json()['status']
	else:
		return "301"


###################################################     '''''''      GPS      ''''''''''         ################################

def gpsLocation(code):
	data = {"vehicleCode":code}
	req = sessionId_.post("http://192.168.43.217:5000/api/gpsLocationCurrent/",json = data)


	if (req.status_code == 201):
		return req.json()['gpsLocation']
	else:
		return "0"


def gpsTracker(code):
	data = {"vehicleCode":code}
	req = sessionId_.post("http://192.168.43.217:5000/api/gpsLocationTrack/",json = data)


	if (req.status_code == 201):
		return req.json()
	else:
		return "0"

def gpsCoveredPaths(code):
	data = {"vehicleCode":code}
	req = sessionId_.post("http://192.168.43.217:5000/api/gpsLocationCovered/",json = data)


	if (req.status_code == 201):
		return req.json()
	else:
		return "0"

#####################################     '''''''      Driving Mode and Camera View     ''''''''''         ################################
def drivingModes(mode,view):
	data = {'mode':mode,'view':view}		# 0-Normal , 1-Remote mode , 2-AutoMode # 0-off , 1-inside camera view , 2-outsideView
	req = sessionId_.post("http://192.168.43.217:5000/api/commands/commandsPassing/",json = data)

'''#############    '''''''       Remote Driving Mode      ''''''''''        #############'''


def remoteCommandsToVehicle(angle_,break_,accelarator_):
	data = {'steerAngle':angle_,'breakFunc':break_,'acccelarationFunc':accelarator_}
	req = sessionId_.post("http://192.168.43.217:5000/api/fromOwner/forRemote/remoteCommandsToVehicle/",json = data)

def retrieveforRC():
	req = sessionId_.get("http://192.168.43.217:5000/api/fromVehicle/forRemote/retrieveforRC/")
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
	req = sessionId_.post("http://192.168.43.217:5000/api/stream/cameraStreamByOwner/",json=data)
	if (req.status_code == 200):
		dec = base64.b64decode(req.content)
		nparr = np.fromstring(dec, np.uint8)
		image_ = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
		pilImage = Image.fromarray(image_)
		byteIO = io.BytesIO()
		pilImage.save(byteIO,format='PNG')
		finalImage = base64.b64encode(byteIO.getvalue())
		return ""+ str(finalImage,'utf-8')
	else:
		return "0"

def validateThroughNotification():
	req = sessionId_.post("http://192.168.43.217:5000/api/vehicle/validateThroughNotification/")
	if (req.status_code == 200):
		return req.json()['isthreat']
	else:
		return "0"

