"""
Created on Sat Jan 21 18:26:09 2017
EE 490 api request example
@author: Stephen West
"""

import requests
import unittest

# simple print resulting dict
url = 'http://10.100.60.199:8080/read_data'
r = requests.get(url)
#store api response in a variable
response = r.json()
# convert temperature to F
response['temperature'] = response['temperature'] * 9/5 + 32
print(response)

## This section of code can test time it takes to run call and
## checks to see if any dictionary items are None or null.
#
#class TempSenseTest(unittest.TestCase):
#    '''tests for connecting to raspberry pi temperature sensor'''
#    
#    def test_connection(self):
#        '''how long does a read on the temperature sensor take'''
#        # simple print resulting dict
#        url = 'http://10.100.60.199:8080/read_data'
#        r = requests.get(url)
#        #store api response in a variable
#        response = r.json()
#        for key, value in response.items():
#            self.assertTrue(response[key])
#
#unittest.main()
