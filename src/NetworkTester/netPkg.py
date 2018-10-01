import traceback

macOUI={"":""}
macIAB={"":""}
extended_ouis=[]

class pkg():
	def __init__(self,data,nw={}):
		self.data=data
		self.reset()
		try:
			self.srcAddr=str(nw['ip_src'])
		except:
			self.srcAddr=None
		try:
			self.srcPort=str(nw['port_src'])
		except:
			self.srcPort=None
		try:
			self.srcMac=self.formatMAC(nw['eth_data'])
			self.dstMac=self.formatMAC(nw['eth_data'][6:])
		except:
			self.srcMac=None
			self.dstMac=None
		try:
			self.dstAddr=str(nw['ip_dst'])
		except:
			self.dstAddr=None
		try:
			self.dstPort=str(nw['port_dst'])
		except:
			self.dstPort=None
		try:
			self.ipprec=nw['ip_tos']>>5
			self.dscp=nw['ip_tos']>>2
		except:
			self.ipprec=None
			self.dscp=None
	def reset(self):
		self.ptr=0
		self.len=len(self.data)		
	def cmpString(self,start,end,str):
		start=start+self.ptr
		end=start+end
		if(end>self.len):
			return False
		return(self.data[start:end]==str)
	def skip(self,num):
		end=self.setEnd(num)
		self.ptr=end
	def setEnd(self,end):
		end=end+self.ptr
		if(end>self.len):
			raise EOFError("pkg reached end of data stream")
		return end
	def getString(self,start,end):
		self.skip(start)
		end=self.setEnd(end)
		s=self.data[self.ptr:end]
		self.ptr=end
		return str(s)
	def getInt8(self,start=0):
		self.skip(start)
		end=self.setEnd(1)
		i=ord(self.data[self.ptr:end])
		self.ptr=end
		return i
	def getInt16(self,start=0):
		self.skip(start)
		end=self.setEnd(2)
		if(end<self.ptr+2):
			return -1
		i=ord(self.data[self.ptr:self.ptr+1])*256
		i=i+ord(self.data[self.ptr+1:self.ptr+2])
		self.ptr=end
		return i
	def getInt32(self,start=0):
		self.skip(start)
		end=self.setEnd(4)
		if(end<self.ptr+4):
			return -1
		i=ord(self.data[self.ptr:self.ptr+1])
		i=i+ord(self.data[self.ptr+1:self.ptr+2])*256
		i=i+ord(self.data[self.ptr+2:self.ptr+3])*256*256
		i=i+ord(self.data[self.ptr+3:self.ptr+4])*256*256*256
		self.ptr=end
		return i
	def getByte(self,start,end):
		self.skip(start)
		end=self.setEnd(end)
		s=self.data[self.ptr:end]
		self.ptr=end
		return bytearray(s)
	def getBitArrayStr(self,start=0):
		value=self.getBitArray(start)
		res=[]
		for i in value:
			if(i):
				res.append("one")
			else:
				res.append("zero")
		return res
	def getBitArray(self,start=0):
		value=self.getInt8(start)
		res=[False,False,False,False,False,False,False,False]
		v=1
		for i in range(8):
			if(value&v>0):
				res[i]=True
			v=v*2			
		return res
	def getHex(self,start=0,end=1):
		s=self.getString(0,end)
		return "0x"+s.encode('hex')
	def jumpStr(self,str):
		pos=self.offsetStr(str)
		if(pos>0):
			self.ptr=self.ptr+pos
	def offsetStr(self,str):
		pos=self.data.find(str,self.ptr)
		if(pos>0):
			return pos-self.ptr
		return -1
	def getMAC(self):
			return self.formatMAC(self.getString(0,6))
	def formatMAC(self,inputStr):
		mac=[]
		for a in range(6):
			s=inputStr[a:a+1]
			mac.append("%02X"%ord(s))
		oui="%s-%s-%s"%(mac[0],mac[1],mac[2])
		if(oui in extended_ouis):
			iab="%s-%s%s%s"%(oui,mac[3],mac[4],mac[5])
			for i in range(6):
				iab=iab[:-1]
				try:
					org=macIAB[iab]
					return "%s (%s)"%(":".join(mac),org)					
				except:
					continue
		try:
			org=macOUI[oui]
			return "%s (%s)"%(":".join(mac),org)
		except:
			print("OUI lookup failed")
		return ":".join(mac)
	def getIP(self):
		return "%d.%d.%d.%d" % (self.getInt8(),self.getInt8(),self.getInt8(),self.getInt8())
		

