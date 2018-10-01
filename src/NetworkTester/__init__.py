import time
from socket import socket, inet_aton, IPPROTO_IP, IP_ADD_MEMBERSHIP
from socket import AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, INADDR_ANY
import struct, select
try:
	from tests import mcastTest,bcastTest
except:
	from NetworkTester.tests import mcastTest,bcastTest
	

class Tester():
	def __init__(self):
		self.tests=[None,None,None,None]
		self.interface="enp0s31f6"
		self.mc=mcastReceiver()
	def addTest(self,obj,nr):
		if(nr>4):
			return
		if(isinstance(obj,mcastTest)):
			self.mc.addSocket(obj.ip,obj.port,obj.read)
		if(isinstance(obj,bcastTest)):
			self.mc.addBSocket(obj.ip,obj.port,obj.read)
		self.tests[nr]=obj.test
	def run(self):
		res=[0,0,0,0,0]
		cnt=0
		res[cnt]=self.testInterfaceStatus()
		if(res[cnt]<2):
			return [res[cnt],0,0,0,0]
		self.mc.rcv(1)
		for a in self.tests:
			cnt=cnt+1
			if(a!=None):
				res[cnt]=a()
		return res
	def testInterfaceStatus(self):
		s = open("/sys/class/net/%s/operstate"%self.interface, 'r').read()
		s=s.strip()
		if(s!="up"):
			return 2
		s = open("/sys/class/net/%s/statistics/rx_crc_errors"%self.interface, 'r').read()
		try:
			s=int(s.strip())
		except:
			s=0
		if(s>0):
			return 3
		return 4



class mcastReceiver:
	def __init__(self):
		self.sock=[]
	def addSocket(self,MCAST_GRP,MCAST_PORT,cb):
		s = socket(AF_INET, SOCK_DGRAM)
		s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		mreq = struct.pack('=4sl', inet_aton(MCAST_GRP), INADDR_ANY) # pack MCAST_GRP correctly
		s.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)         # Request MCAST_GRP
		s.bind((MCAST_GRP, MCAST_PORT))                           # Bind to all intfs
		self.sock.append((s,cb))
	def addBSocket(self,ADDR,PORT,cb):
		s = socket(AF_INET, SOCK_DGRAM)
		s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		s.bind((ADDR, PORT))
		self.sock.append((s,cb))
	def rcv(self,timeout):
		i=[]
		for a in self.sock:
			i.append(a[0])
		readable, writable, exceptional = select.select(i, [], [],timeout)
		for s in readable:
			for a in self.sock:
				if(s==a[0]):
					data, srv_sock = s.recvfrom(2000)              # Receive data (blocking)
					a[1](data,srv_sock)



				
if __name__ == '__main__':
	from tests import Audio
	from tests import Lights
	app=Tester()
	app.addTest(Audio.testPTP(),0)
	app.addTest(Audio.testDante(),1)
	app.addTest(Audio.testLake(),2)
	app.addTest(Lights.testACN(),3)
	res=app.run()
	print(res)
	
