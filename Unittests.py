import unittest

from hypothesis.core import given
from ASOS_Webscraper import AsosScraper 
from selenium import webdriver 
import hypothesis.strategies as st 


class ASOS_Webscraper_Tests(unittest.TestCase):

    def setUp(self):
        self.AsosScraper = AsosScraper(webdriver.Chrome(),'men')
    
    @given(st.just('//button[@class="g_k7vLm _2pw_U8N _2BVOQPV"]'))
    def test_accept_cookies(self, xpath):
        self.assertEqual('//button[@class="g_k7vLm _2pw_U8N _2BVOQPV"]')
        


    def tearDown(self):
        del self.AsosScraper

    

unittest.main(argv=[''], verbosity=2, exit=False)
        
# Test that the functions goes to websites. 
# In hypothesis, there's a module which tests URLs.
# For accept cookies, could send a bunch of xpaths which share the element of the 
# accept cookies button and see if it doesn't give an exception. 

