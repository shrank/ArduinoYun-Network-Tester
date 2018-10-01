try:
	from tests import mcastTest,testTime,testSource
	from protocols import acn
	from netPkg import pkg
except:	
	from NetworkTester.tests import mcastTest,testTime,testSource
	from NetworkTester.protocols import acn
	from NetworkTester.netPkg import pkg


class testACN(testTime,testSource,mcastTest):
	def __init__(self):
		mcastTest.__init__(self)
		testSource.__init__(self)
		testTime.__init__(self)
		self.port=5568
		self.ip="239.255.0.1"
		self.pkt=0
		self.version=0
	def read(self,data,srv):
		p=acn.ACN()
		pkt=pkg(data)
		self.pkt=p.parse(pkt)
		testTime.read(self,data,srv)		
		testSource.read(self,data,srv)
	def test(self):
		res=self.testTime(None,2,10)
		if(res<4):
			return res
		res=self.testSource()
		if(res<4):
			return res
		if(self.pkt['protocol']['name']!='sACN E1.31'):
			return 3
		return 4
