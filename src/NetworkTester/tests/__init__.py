import time


class genericTest:
	def __init__(self):
		pass
	def test(self):
		return 0		

class extTest(genericTest):
	def __init__(self):
		genericTest.__init__(self)
		self.cmd=""
	def read(self,returncode,ouput,error):
		pass

class mcastTest(genericTest):
	def __init__(self):
		genericTest.__init__(self)
		self.port=0
		self.ip=""
	def read(self,data,srv):
		pass

class bcastTest(genericTest):
	def __init__(self):
		genericTest.__init__(self)
		self.port=0
		self.ip=""
	def read(self,data,srv):
		pass

class testTime():
	def __init__(self):
		self.last=0
		self.warn=0
		self.warntime=1
	def read(self,data,srv):
		self.last=time.time()
	def testTime(self,Warn,Error,Off):
		w=time.time()-self.warn
		if(w<self.warntime):
			return 3
		t=time.time()-self.last
		if(Off !=None and t>Off):
			return 1
		if(Error !=None and t>Error):
			return 2
		if(Warn !=None and t>Warn):
			self.warn=time.time()
			return 3
		return 4

class testSource():
	def __init__(self):
		self.source=""
		self.change=False
		self.warn=0
		self.warntime=1
	def read(self,data,srv):
		if(self.source!=srv[0]):
			if(self.source!=""):				
				self.change=True
			self.source=srv[0]
	def testSource(self):
		w=time.time()-self.warn
		if(w<self.warntime):
			return 3
		if(self.change):
			self.warn=time.time()
			self.change=False
			return 3
		return 4