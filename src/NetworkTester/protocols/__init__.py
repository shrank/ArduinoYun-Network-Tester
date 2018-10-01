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


import traceback

class Stream():
	def __init__(self):
		self._data={'nw':{},"protocol":{},"hostname":"",'stats':{'EOF':0,'Parser':0}}
		self.infoStr=""
	def __getitem__(self,k):
		return self._data[k]
	def getValue(self,k):
		try:
			return self[k]
		except:
			return None
	def getStr(self,k):
		try:
			return str(self[k])
		except:
			return ""
	def __setitem__(self,k,v):
		self.last=v
		self._data[k]=v
	def setValue(self,k,v):
		self[k]=v	
	def getLast(self):
	   return self.last
	def getData(self):
		return self._data

class parserTemplate():
	def __init__(self):
		self.description="DUMMY"
		self.handlers=[]
	def parse(self,pkt):
		u=Stream()
		try:
			u=self.runParser(pkt,u)
		except:
			print("----------------------------------------------------------------------------\n")
			traceback.print_exc()
			print("----------------------------------------------------------------------------\n")
			return None
		return u
	def getDesc(self):
		return self.description
	def getHandlers(self):
		return self.handlers
	def runParser(self,pkt,u):
		return u

