import time
import unittest
import sys
sys.path.insert(0,"../")
from tests import testTime, result

class TestTime(unittest.TestCase):

	def test_parseOK(self):
		a=testTime()
		self.assertTrue(a.testTime(None,0.11,0.22)<=result.OFF)
		a.read(None,{})
		self.assertTrue(a.testTime(None,0.11,0.22)==result.OK)
		time.sleep(1)
		self.assertTrue(a.testTime(None,1,2)==result.FAIL)
		time.sleep(2)
		self.assertTrue(a.testTime(None,1,2)==result.OFF)		

	def test_parseWarn(self):
		a=testTime()
		a.read(None,{})
		self.assertTrue(a.testTime(10,11,11)==result.OK)
		self.assertTrue(a.testTime(0,1,1)==result.WARN)
		self.assertTrue(a.testTime(10,11,11)==result.WARN)
		time.sleep(0.9)
		self.assertTrue(a.testTime(10,11,11)==result.WARN)
		time.sleep(1)
		self.assertTrue(a.testTime(10,11,11)==result.OK)


if __name__ == '__main__':
    unittest.main()
