import time
import unittest
import sys
sys.path.insert(0,"../")
from tests import Audio

class TestStatusPkt(unittest.TestCase):

	def test_parseLong(self):
		data="\x15\x33\xd4\x01\x90\x0d\x23\x17\xfe\xff\xff\xff\xfd\xff\xff\xff\x01\x00\x00\x00\x64\x00\x09\x00\x4e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1b\xd3\x39\x20\x8f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x74\x69\x97\xe6"
		a=Audio.testLake()
		a.read(data,["169.55.33.22",234])
		self.assertTrue(a.test()==4)
		time.sleep(1.1)
		self.assertTrue(a.test()==4)
		time.sleep(1)
		self.assertTrue(a.test()==2)
		time.sleep(1.5)
		self.assertTrue(a.test()==1)
		a.read(data,["169.55.33.23",234])
		self.assertTrue(a.test()==3)
		a.read(data,["169.55.33.23",234])
		self.assertTrue(a.test()==3)
		time.sleep(1)
		a.read(data,["169.55.33.23",234])
		self.assertTrue(a.test()==4)





if __name__ == '__main__':
    unittest.main()
