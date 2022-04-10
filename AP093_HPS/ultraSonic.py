import time
import gpiopy as gp

gp.gpioExport(1851)
gp.gpioExport(1852)

gp.gpioDirec(1851,'out')
gp.gpioDirec(1852,'in')

try:
	while True:
		var = gp.gpioRead(1852)
		gp.gpioValue(1851,1)
		time.sleep(0.00001)
		gp.gpioValue(1851,0)
		while(str(var) == '0'):
			start = time.time()
		var=gp.gpioRead(1852)
		while(str(var) == '1'):
			stop = time.time()
		var=gp.gpioRead(1852)
		duration = stop - start
		distance = duration * 17150
		print("distance",distance)
		time.sleep(1)
except KeyboardInterrupt:
	print("I'm stopping ultrasonic reading..Thank you")

gp.gpioClear(1851)
gp.gpioClear(1852) 
