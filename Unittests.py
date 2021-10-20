import unittest
from ASOS_Webscraper import AsosScraper 
from selenium import webdriver 
import hypothesis

# import unittest
# from example.cart import ShoppingCart
# from example.product import Product
class ASOS_Webscraper_Tests(unittest.TestCase):

    def setUp(self):
        self.AsosScraper = AsosScraper(webdriver.Chrome(),'men')
        
    def test_go_to_website(self):
        # expected_value = "https://www.asos.com/men"    
        self.assertTrue(webdriver.Chrome().get("https:/www.asos.com/men"))
    # def number_of_extracted_urls(self):
    #     expected_value = 72
    #     actual_value = print(len(self.links))
    #     self.assertEqual(expected_value,actual_value)

    
      


    def tearDown(self):
        del self.AsosScraper

    

unittest.main(argv=[''], verbosity=2, exit=False)
        
# Test that the functions goes to websites. 
# In hypothesis, there's a module which tests URLs.
# For accept cookies, could send a bunch of xpaths which share the element of the 
# accept cookies button and see if it doesn't give an exception. 

