try:
	from tests import extTest
except:	
	from NetworkTester.tests import extTest


class testfPing(extTest):
	def __init__(self,target):
		extTest.__init__(self)
		self.cmd="/usr/sbin/fping -c 100 -i 1 -p 10 -b 1472 -q "+target
		self.loss=None
		self.times=None
		self.maxTime=1.0
	def read(self,returncode,output):
		line=output.split()
		self.loss=line[4].split("/")
		try:
			self.times=line[7].split("/")
		except:
			self.times=[100,100,100]
		for i in range(3):
			self.times[i]=float(self.times[i])
	def test(self):
		if(self.loss==None or self.times==None):
			return 1
		if(self.loss[2]!="0%"+","):
			return 2
		print(self.times)
		if(self.times[1]>self.maxTime):
			return 3
		return 4
