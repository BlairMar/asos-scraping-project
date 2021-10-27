import unittest

from hypothesis.core import given
from ASOS_Webscraper import AsosScraper 
from selenium import webdriver 
import hypothesis.strategies as st 


class ASOS_Webscraper_Tests(unittest.TestCase):

    scraper_links = AsosScraper(driver = webdriver.Chrome, gender = 'men')
    scraper_links = AsosScraper.extract_links
    def setUp(self):
        self.driver = webdriver.Chrome()
        
        # self.driver.get("https://www.asos.com/men")
       
     

  

    # def test_go_to_website(self):
    #     self.driver = webdriver.chrome() 
    #     self.driver.get("https://www.asos.com/men")
    #     self.assertTrue(self.driver)
    
   
    # def test_accept_cookies(self):
    #     xpath = '//button[@class="g_k7vLm _2pw_U8N _2BVOQPV"]'
    #     expected_value = self.driver.find_element_by_xpath(xpath)
    #     actual_value = AsosScraper.accept_cookies_button('//button[@class="g_k7vLm _2pw_U8N _2BVOQPV"]')
    #     self.assertEqual(expected_value, actual_value)

        # '//button[@class="g_k7vLm _2pw_U8N _2BVOQPV"]'
        
        # Webelement 
        # <selenium.webdriver.remote.webelement.WebElement 
        # (session="be4677ff5a73456b180d5f25371fdfe5",
        #  element="f83d42a9-b4f2-4396-8537-b26929e4ea3a")>

    def test_example(self):
        # scraper_links = AsosScraper.extract_links('//*[@id="029c47b3-2111-43e9-9138-0d00ecf0b3db"]/div/div[2]/ul/li[1]/ul/li[*]')
        for element in   self.scraper_links.extract_links():
            if element.slice(0,8,1) == "https://":
                expected_value = True 
            else: 
                expected_value = False 
            
        actual_value = self.links 
        self.assertEqual(expected_value, actual_value)

    # list should contain strings with URLs inside 
    # self.links string starts with. https:// 

    # def tearDown(self):
    #     del self.scraper_links.close()

 

unittest.main(argv=[''], verbosity=2, exit=False)

# if name == __main__:

        
# Test that the functions goes to websites. 
# In hypothesis, there's a module which tests URLs.
# For accept cookies, could send a bunch of xpaths which share the element of the 
# accept cookies button and see if it doesn't give an exception. 

