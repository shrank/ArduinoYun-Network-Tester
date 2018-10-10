try:
	from tests import extTest
except:	
	from NetworkTester.tests import extTest


class testPing(extTest):
	def __init__(self,target,c):
		extTest.__init__(self)
		self.cmd="ping -c %d -W 1 -s 1472 -q %s "%(c,target)
		self.loss=None
		self.times=None
		self.count=4
		self.maxTime=1.0
	def read(self,returncode,output,err):
		print(output)
		lines=output.split("\n")
		try:
			line=lines[len(lines)-3]
			line=line.split()
			self.loss=int(line[6].strip('%'))
		except:
			self.loss=100
		try:
			line=lines[len(lines)-2]
			line=line.split()
			self.times=line[3].split("/")
		except:
			self.times=[100,100,100]
		for i in range(len(self.times)):
			self.times[i]=float(self.times[i])
	def test(self):
		if(self.loss==None or self.times==None):
			return 1
		if(self.loss==100):
			return 2
		if(self.times[1]>self.maxTime or self.loss>0):
			return 3
		return 4
