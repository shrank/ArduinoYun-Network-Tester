try:
	from tests import extTest,result
except:
	from NetworkTester.tests import extTest,result

# test IP address, used with DHCP-enabled interfaces

class testIP(extTest):
	def __init__(self,interface,allowed=[]):
		extTest.__init__(self)
		self.cmd="ifconfig "+interface
		self.allowed=allowed
		self.ip=""
	def read(self,returncode,output,err):
		self.ip=""
		lines=output.split("\n")
		for a in lines:
			a=a.strip()
			if(a.startswith("inet addr:")):
				a=a.split(":")
				a=a[1].split(" ")
				self.ip=a[0].strip()
			elif(a.startswith("inet ")):
				a=a.split(" ")
				self.ip=a[1].strip()
	def test(self):		
		if(self.ip==""):
			return result.FAIL
		if(len(self.allowed)==0):
			return result.OK
		for a in self.allowed:
			if(self.ip.startswith(a)):
				return result.OK
		return result.WARN




if __name__ == '__main__':
	a= testIP()
	print(a.test)