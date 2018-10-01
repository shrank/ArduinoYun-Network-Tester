# Name: Artnet Scanner
# 
# Author: Michael Salathe
# Version: 0.1
# Copyright 2013 Michael Salathe
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

try:
	import netPkg
	from protocols import parserTemplate
except:
	import NetworkTester.netPkg
	from NetworkTester.protocols import parserTemplate

import sys, traceback

groupArtnetSACN={
"int":{"text":"Protocol Internals","desc":"Protocol Flags","ord":4}
,"dmx":{"text":"DMX","desc":"DMX details","ord":3}
,"node":{"text":"Node","desc":"Node Information","ord":2}
}
descSACN={
"ip_dst":{"desc":"239.255.Universe-Hi.Universe-Lo","group":"net"}
,"Root Flags":{"desc":"Protocol flags: len:0 vec:1 hdr:1 data:1","group":"int"}
,"Root Vector":{"desc":"Identifies RLP Data as 1.31 Protocol PDU: 0x00000003","group":"int"}
,"cid":{"desc":"RFC 4122 UUID. Should maintain the same CID for its entire lifetime","group":"node"}
,"Frame Flags":{"desc":"Protocol flags: len:0 vec:1 hdr:1 data:1","group":"int"}
,"Frame Vector":{"desc":"Identifies 1.31 data as DMP Protocol PDU: 0x00000002","group":"int"}
,"Source Name":{"desc":"User Assigned Name of Source","group":"node"}
,"priority":{"desc":"Data priority if multiple sources. 0-200, default of 100","group":"node"}
,"DMP Flags":{"desc":"Protocol flags: len:0 vec:1 hdr:1 data:1","group":"int"}
,"DMP Vector":{"desc":"Identifies DMP Set Property Message PDM: 0x02","group":"int"}
,"atype":{"desc":"Identifies format of address and data. Receivers shall discard the packet if the received value is not 0xa1.","group":"int"}
,"number":{"desc":"Identifier for a distinct stream of DMX Data. 1-63999 possible","group":"dmx"}
,"startaddr":{"desc":"Indicates DMX START Code is at DMP address 0","group":"dmx"}
,"inc":{"desc":"Indicates each property is 1 octet","group":"dmx"}
,"lenght":{"desc":"Indicates 1+ the number of slots in packet","group":"dmx"}
,"seq":{"text":"Sequence Nr","desc":"packet sequence number","group":"dmx"}
,"proto":{"text":"Protocol Version","desc":"Protocol Version Details","ord":1}
,"startcode":{"desc":"","group":"dmx"}
}

class ACN(parserTemplate):
	def __init__(self):
		parserTemplate.__init__(self)
		self.handlers.append({"dstPort":5568})
		self.description="sACN E1.31, ACN E1.17(Experimental)"
	def runParser(self,data,u):
		version=0
		name_len=32
		header="\0\x10\0\0ASC-E1.17\0\0\0"
		u.setValue("type","Universe")
		if(data.cmpString(0,len(header),header)==False):
			return 0
		data.skip(len(header))
		(flen,fvec,fhdr,fdata)=ACN.acn_get_flags(data.getBitArray())
		u.setValue("Root Flags","len:%d vec:%d hdr:%d data:%d"%(flen,fvec,fhdr,fdata))
		data.skip(1)
		if(fdata==False):
			raise EOFError("Data bit not set")
		if(flen):
			data.skip(1)
		u.setValue("Root Vector",data.getHex(0,4))
		if(u.getLast()=="0x00000003"):
			u['protocol']['name']="ACN draft"
			version=1
		else:
			if(u.getLast()=="0x00000004"):
				u['protocol']['name']="sACN E1.31"
				version=31
				name_len=64
			else:
				raise Exception("Wrong PDU")
		u.setValue("cid",ACN.acn_uuid_format(data.getString(0,16)))
		(flen,fvec,fhdr,fdata)=ACN.acn_get_flags(data.getBitArray())
		u.setValue("Frame Flags","len:%d vec:%d hdr:%d data:%d"%(flen,fvec,fhdr,fdata))
		data.skip(1)
		if(fdata==False):
			raise EOFError("Data bit not set")
		if(flen):
			data.skip(1)
		u.setValue("Frame Vector",data.getHex(0,4))
		if(u.getLast()!="0x00000002"):
				raise Exception("Wrong PDU")
		u.setValue("hostname",data.getString(0,name_len).rstrip('\0'))
		u.setValue("priority",data.getInt8())
		if(version==31):
			data.skip(2)
		u.setValue("seq",data.getInt8())
		if(version==31):
			data.skip(1)
		u.setValue("number",data.getInt16())
		u.infoStr="Universe %d from \"%s\", " % (u.getLast(),u["hostname"])
		u.setValue("lenght",0)
		u.data=[]
		(flen,fvec,fhdr,fdata)=ACN.acn_get_flags(data.getBitArray())
		u.setValue("DMP Flags","len:%d vec:%d hdr:%d data:%d"%(flen,fvec,fhdr,fdata))
		data.skip(1)
		if(fdata==False):
			raise EOFError("Data bit not set")
		if(flen):
			data.skip(1)
		u.setValue("DMP Vector",data.getHex())
		if(u.getLast()!="0x02"):
			raise Exception("Wrong PDM")
		u.setValue("atype",data.getHex())
		if(u.getValue("atype")!="0xa1"):
			raise Exception("Wrong adress type")
		if(version<31):
			u.setValue("startcode",data.getHex())			
			data.skip(1)
		else:
			u.setValue("startaddr",data.getInt16())
		u.setValue("inc",data.getInt16())
		u.setValue("lenght",data.getInt16())
		u.infoStr=u.infoStr+"len: %d, prio: %d" % (u.getLast(),u["priority"])
		if(version==31):
			u.setValue("startcode",data.getHex())
		u.setValue("dmxData",data.getByte(0,u.getValue("lenght")-1))
		return u
	@staticmethod
	def acn_get_flags(data):
		d=data[4]
		h=data[5]
		v=data[6]
		l=data[7]
		return (l,v,h,d)
	@staticmethod
	def acn_uuid_format(data):
		res=""
		for x in data:
			res=res+x.encode('hex')
		split=[8,4,4,4]
		c=0
		for i in split:
			c+=i
			if(len(res)>c):
				res=res[:c]+"-"+res[c:]
				c+=1
		return res
