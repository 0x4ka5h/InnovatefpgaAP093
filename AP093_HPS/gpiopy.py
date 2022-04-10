import time
from os import chmod
def gpioExport(pin):
	try:
		chmod('/sys/class/gpio/export',0o777)
		exp=open('/sys/class/gpio/export','r+')
		exp.write(str(pin))
		exp.seek(0)
		exp.close()
	except:
		print("Pin already exported or wrong pin number")

def gpioClear(pin):
	try:
		chmod('/sys/class/gpio/unexport',0o777)
		unexp=open('/sys/class/gpio/unexport','r+')
		unexp.write(str(pin))
		unexp.seek(0)
		unexp.close()
	except:
		print("Pin already unexported or wrong pin number")
def gpioDirec(pin,dirc):
	try:
		gp1=open('/sys/class/gpio/gpio'+str(pin)+'/direction','r+')
		gp1.write(dirc)
		gp1.seek(0)
		gp1.close()
	except:
		print("Enter in/out only or wrong pin entered")
def gpioValue(pin,val):
	try:
		gp2=open('/sys/class/gpio/gpio'+str(pin)+'/value','r+')
		gp2.write(str(val))
		gp2.seek(0)
		gp2.close()
	except:
		print("Enter 0/1 only or wrong pin entered")
def gpioRead(pin):
	try:
		val=0
		gp=open('/sys/class/gpio/gpio'+str(pin)+'/value','r+')
		val=gp.read()
		gp.seek(0)
		gp.close()
	except:
		print("Enter 0/1 only or wrong pin entered")
	return val

 
