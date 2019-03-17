import time

class result:
	OFF=1
	FAIL=2
	WARN=3
	OK=4

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
			return result.WARN
		t=time.time()-self.last
		if(Off !=None and t>Off):
			return result.OFF
		if(Error !=None and t>Error):
			return result.FAIL
		if(Warn !=None and t>Warn):
			self.warn=time.time()
			return result.WARN
		return result.OK

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
			return result.WARN
		if(self.change):
			self.warn=time.time()
			self.change=False
			return result.WARN
		return result.OK