import asyncio
from os import *
from math import *
import time
from package.basecomnios import *
import threading
import requests
import gpiopy

#system("chmod 777 /sys/class/gpio/export")
#system("echo 107 > /sys/class/gpio/export")
#system("echo out > /sys/class/gpio/gpio107/direction")
#system("echo 1 > /sys/class/gpio/gpio107/value")


'''
{
    "RFS": {
        "gSensorData": {
            "gSensor": {
                "x": 1.5103109414596727,
                "y": 5.468665712195788,
                "z": 8.361845070040161
            }
        },
        "rfsData": {
            "lux": 134.02087940847585,
            "humidity": 46.736825925140714,
            "temperature": 41.46854218998822,
            "mpu9250": {
                "ax": 60.89765502875218,
                "ay": -15.244680827962398,
                "az": -24.29826992695648,
                "gx": -6.05319156694371,
                "gy": 6.96850206625556,
                "gz": -7.483049198958498,
                "mx": -84.36140005907677,
                "my": -6.411592567195299,
                "mz": 42.03987671550894
            }
        }
    }
}
'''


gSensor = {'x':0,'y':0,'z':0}
mpu9250 = {}

check = 0

aX , l_aX = 0, 0
aY , l_aY = 0, 0
aZ , l_aZ = 0, 0

check = 0


async def take_(j):
	global gSensor,mpu9250, aX, aY, aZ
	gSensor = j['gSensorData']['gSensor']
	mpu9250 = j['rfsData']['mpu9250']

	#aX = gSensor['x'] 
	aX = mpu9250['ax']
	#aY = gSensor['y']
	aY = mpu9250['ay']
	#aZ = gSensor['z']
	aZ = mpu9250['az']
	
	#logger.debug(aX,aY,aZ)

### assumptions

async def detectTowing():
	global check
	global l_aX,l_aY,l_aZ,aX,aY,aZ
	while True :
		try:
			if (l_aX!=0 or l_aY!=0 or l_aZ!=0):
				if(((abs(aX-l_aX))>200 or (abs(aY-l_aY))>200)  and 
				((abs(aX-l_aX))>200 or (abs(aZ-l_aZ))>200) and 
				((abs(aY-l_aY))>200 or (abs(aZ-l_aZ))>200)):	
					d = {'yn':1}
					requests.post('http://10.4.44.130:5001/api/Towing/',json=d)	
					

				if(	(abs(aX-l_aX))>300 or (abs(aY-l_aY))>300 or (abs(aZ-l_aZ))>300):
					print("\n[Alert]  towing Detected .. +_+")
					d = {'yn':1}
					requests.post('http://10.4.44.130:5001/api/Towing/',json=d)	
			print(aX,aY,aZ)
			print(l_aX,l_aY,l_aZ)
				
			
			if (check%50==0):
				l_aX = aX
				l_aY = aY
				l_aZ = aZ
				check+=1
				
			if (x!=aX and y!=aY and z!=aZ ):
				check+=1
				
			x = aX
			y = aY
			z = aZ
			time.sleep(7)
		except:
			logger.debug("oMkay")
			time.sleep(60)
			d = {'yn':1}
			requests.post('http://10.4.44.130:5001/api/Towing/',json=d)	
			gpiopy.gpioExport(1805)
			gpiopy.gpioDirec(1805,"out")
			gpiopy.gpioValue(1805,1)


asyncio.run(detectTowing(),debug=True)
