import time
import unittest
from handler import handle

class TestHandle(unittest.TestCase):

  def test_load(self):
    failures = 0
    for x in range(20): 
      print('Request #: ', x)

      response = handle()
      print('Response Code: ', response.status_code)
      if response.status_code != 200:
        print('FAILED')
        failures += 1
      else:
        print('PASS')
      
      time.sleep(5.0)

    self.assertEqual(failures, 0)

if __name__ == '__main__':
    unittest.main()