import time
import unittest
import sys
sys.path.insert(0,"../")
from tests import testTime

class TestTime(unittest.TestCase):

	def test_parseOK(self):
		a=testTime()
		self.assertTrue(a.testTime(None,0.11,0.22)<=1)
		a.read(None,{})
		self.assertTrue(a.testTime(None,0.11,0.22)==4)
		time.sleep(1)
		self.assertTrue(a.testTime(None,1,2)==2)
		time.sleep(2)
		self.assertTrue(a.testTime(None,1,2)==1)				

	def test_parseWarn(self):
		a=testTime()
		a.read(None,{})
		self.assertTrue(a.testTime(10,11,11)==4)
		self.assertTrue(a.testTime(0,1,1)==3)
		self.assertTrue(a.testTime(10,11,11)==3)
		time.sleep(0.9)
		self.assertTrue(a.testTime(10,11,11)==3)
		time.sleep(1)
		self.assertTrue(a.testTime(10,11,11)==4)


if __name__ == '__main__':
    unittest.main()
