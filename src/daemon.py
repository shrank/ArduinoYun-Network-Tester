#!/usr/bin/python

from NetworkTester import Tester
from NetworkTester.tests import Audio, Lights, Ping
import traceback
from bridge.bridgeclient import BridgeClient as bridgeclient





app=Tester()
app.interface="eth1"
app.addTest(Audio.testPTP(),0)
app.addTest(Audio.testDante(),1)
app.addTest(Audio.testLake(),2)
app.addTest(Lights.testACN(),3)

f=0
client = bridgeclient()

while True:
	try:
		res=app.run()
	except:
		print(traceback.print_exc())
		res=[0,0,0,0,0]
	try:
		client.put('LED', "%d\n%d\n%d\n%d\n%d\n"%(res[0],res[1],res[2],res[3],res[4]))
	except:
		print(traceback.print_exc())
		client = bridgeclient()
		
