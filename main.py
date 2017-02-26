# Watches nearby BT and WIFI 
# buzzes when target within some range

# Written by Chase McCarty, January 2017


from wifi import WifiThread
from bt import BtThread
import threading
import time
import Queue

threads = []

buzzBt = False
buzzWifi = False


def main():
	# make sure these are lower case
	targetWifiMacs = ["44:00:10:3f:2a:b7"]
	targetBTMacs = ["44:00:10:3f:2a:b8", "00:1a:7d:da:71:13"]
	targetWifiDistance = -65
	targetBTDistance = -65
	scanTime = 12

	# Queue objects for communicating with threads
	wifiQueue = Queue.Queue()
	btQueue = Queue.Queue()

	threads = [WifiThread("mon0", targetWifiMacs, targetWifiDistance, wifiQueue), BtThread(targetBTMacs, targetBTDistance, btQueue)]

	for thread in threads:
		thread.start()

	while True:
		printBuzzer(wifiQueue, btQueue)
		time.sleep(scanTime)

def printBuzzer(wifiQueue, btQueue):	
	global buzzBt
	global buzzWifi

	if not wifiQueue.empty():
		buzzWifi = False
		while(not wifiQueue.empty()):
			wifiTuple = wifiQueue.get()
			#print("seen Wifi " + str(wifiTuple[1]))
			buzzWifi = (buzzWifi or wifiTuple[0])

	if not btQueue.empty():
		print("BT Queue not empty")
		buzzBt = False
		while(not btQueue.empty()):
			btTuple = btQueue.get()
			#print("seen BT " + str(btTuple[1]))
			buzzBt = (buzzBt or btTuple[0])
	else:
		print("BT Queue empty")

	print("")

	if buzzWifi == True:
		print("Wifi is on")
	elif buzzWifi == False:
		print("Wifi is off")

	if buzzBt == True:
		print("Bt is on")
	elif buzzBt == False:
		print("Bt is off")

	print("")

	'''
	if buzzWifi == True and buzzBt == True:
		print("Wifi is on, BT is on")
	elif buzzWifi == True and buzzBt == False:
		print("Wifi is on, BT is off")
	elif buzzWifi == False and buzzBt == True:
		print("Wifi is off, BT is on")
	else:
		print("Wifi is off, BT is off")
	'''

try:
	main()
except KeyboardInterrupt:
	for thread in threads:
		thread.kill()
