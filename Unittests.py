import unittest
from ASOS_Webscraper import AsosScraper 
from selenium import webdriver 

class ASOS_Webscraper_Tests(unittest.TestCase):

    def setUp(self):
        self.AsosScraper = AsosScraper("https://www.asos.com/", "men")
        
    def go_to_website(self):
        expected_value = "https://www.asos.com/men"
        actual_value = driver.get(URL)
        self.assertEqual(expected_value, actual_value)


    def tearDown(self):
        del = self.AsosScraper

    

unittest.main(argv=[''], verbosity=2, exit=False)
        
        