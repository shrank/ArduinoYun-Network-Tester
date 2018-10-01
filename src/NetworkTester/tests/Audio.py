try:
	from tests import mcastTest,bcastTest,testTime,testSource
	from netPkg import pkg
except:
	from NetworkTester.tests import mcastTest,bcastTest,testTime,testSource
	from NetworkTester.netPkg import pkg


class testDante(testTime,mcastTest):
	def __init__(self):
		mcastTest.__init__(self)
		testTime.__init__(self)
		self.port=8708
		self.ip="224.0.0.233"		
		self.dante_seq=0
	def read(self,data,srv):
		pkt=pkg(data)
		pkt.skip(4)
		seq=pkt.getInt16()
		pkt.skip(10)
		if(pkt.cmpString(0,8,"Audinate")):
			self.dante_seq=seq
			testTime.read(self,data,srv)
			self.source=srv[0]
	def test(self):
		res=self.testTime(1,None,2)
		if(res<4):
			return res
		if(self.source[0:4]=="172."):
			return 2
		return 4

class testPTP(testTime,testSource,mcastTest):
	def __init__(self):
		mcastTest.__init__(self)
		testTime.__init__(self)
		testSource.__init__(self)
		self.port=319
		self.ip="224.0.1.129"
	def read(self,data,srv):
		pkt=pkg(data)
		version=pkt.getInt16()
		NWversion=pkt.getInt16()
		domain=pkt.getString(0,16).strip()
		if(not pkt.getInt8()==1):
			return
		if(not pkt.getInt8()==1):
			return
		pkt.skip(10)
		if(not pkt.getInt8()==0):
			return
		testTime.read(self,data,srv)
		testSource.read(self,data,srv)
	def test(self):
		res=self.testTime(None,0.5,2)
		if(res<4):
			return res
		res=self.testSource()
		if(res<4):
			return res
		return 4



class testLake(testTime,testSource,bcastTest):
	def __init__(self):
		bcastTest.__init__(self)
		testSource.__init__(self)
		testTime.__init__(self)
		self.ip="255.255.255.255"
		self.port=6017
	def read(self,data,srv):
		testTime.read(self,data,srv)
		testSource.read(self,data,srv)
	def test(self):
		res=self.testTime(None,2,3)
		if(res<4):
			return res
		res=self.testSource()
		if(res<4):
			return res
		return 4
