import unittest

from hypothesis.core import given
from ASOS_Webscraper import AsosScraper 
from selenium import webdriver 
import hypothesis.strategies as st 


class ASOS_Webscraper_Tests(unittest.TestCase):

    
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        
        # navigate to the application home page
        self.driver.get("http://www.asos.com/men")
        
       
     

  

    # def test_go_to_website(self):
    #     self.driver = webdriver.chrome() 
    #     self.driver.get("https://www.asos.com/men")
    #     self.assertTrue(self.driver)
    

        # '//button[@class="g_k7vLm _2pw_U8N _2BVOQPV"]'
        
        # Webelement 
        # <selenium.webdriver.remote.webelement.WebElement 
        # (session="be4677ff5a73456b180d5f25371fdfe5",
        #  element="f83d42a9-b4f2-4396-8537-b26929e4ea3a")>

    # Successful Unittest! 
    def test_example(self):
        test_list = self.driver.find_elements_by_xpath('//*[@id="029c47b3-2111-43e9-9138-0d00ecf0b3db"]/div/div[2]/ul/li[1]/ul/li[1]')
        print(test_list)
        number_of_items = len(test_list)
        self.assertIsInstance(test_list, list)
        


    # list should contain strings with URLs inside 
    # self.links string starts with. https:// 

    # def tearDown(self):
    #     del setUp(self)

 

unittest.main(argv=[''], verbosity=2, exit=False)

# if name == __main__:

        
# Test that the functions goes to websites. 
# In hypothesis, there's a module which tests URLs.
# For accept cookies, could send a bunch of xpaths which share the element of the 
# accept cookies button and see if it doesn't give an exception. 

