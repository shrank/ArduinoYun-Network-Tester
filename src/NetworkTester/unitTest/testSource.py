import time
import unittest
import sys
sys.path.insert(0,"../")
from tests import testSource

class TestSource(unittest.TestCase):

	def test_parseOK(self):
		a=testSource()
		a.read(None,["192.168.1.1","556"])
		self.assertTrue(a.testSource()==4)
		a.read(None,["192.168.1.1","556"])
		self.assertTrue(a.testSource()==4)
		a.read(None,["192.168.1.2","556"])
		self.assertTrue(a.testSource()==3)
		a.read(None,["192.168.1.2","556"])
		self.assertTrue(a.testSource()==3)
		time.sleep(1)
		a.read(None,["192.168.1.2","556"])
		self.assertTrue(a.testSource()==4)


if __name__ == '__main__':
    unittest.main()
