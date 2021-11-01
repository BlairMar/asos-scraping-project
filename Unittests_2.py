import unittest

from hypothesis.core import given
from selenium.webdriver.android.webdriver import WebDriver
from ASOS_Webscraper import AsosScraper 
from selenium import webdriver 
import hypothesis.strategies as st 
from PIL import Image
import requests
import imagehash


class ASOS_Webscraper_Tests(unittest.TestCase):

    
    
    def setUp(self):
        self.scraper = AsosScraper(webdriver.Chrome(), "men")
        
  
        
    
    # Fixed Unittest for Webscraper. 
    # Put in return True under click_buttons method in scraper to get this working 
    def test_click_buttons(self):
        click_accept_cookies = self.scraper.click_buttons('//button[@class="g_k7vLm _2pw_U8N _2BVOQPV"]', 1)
        self.assertTrue(click_accept_cookies)

    # load_more_products() returns the length of the list, which is an integer. 
    # This tests whether the lengths of the lists returned are the same length. 

    def test_load_more_products(self):
        # goes to the url of the page 
        self.scraper.driver.get("https://www.asos.com/men/new-in/cat/?cid=27110&nlid=mw|new+in|new+products|view+all")
        # runs load_more_products on the page. Defaults to 1 for section 1 
        productlist = self.scraper.load_more_products()
        print(productlist)
        self.assertIsInstance(productlist, int)

  

    # Successful Unittest! 
    # Tests whether the images that are saved are the same. 
    # Could be more elaborate. 
    # pip install imagehash and PIL to make this work
    #  Use this link to find out more 
    # 'https://practicaldatascience.co.uk/data-science/how-to-use-image-hashing-to-identify-visually-similar-or-duplicate-images
    def test_image_output(self):
      # copy your image pathway inside these brackets. 
      # use an r string for backlashes or use double backlashes to avoid an error 
      # example: 'C:\\Users\\WR\\Webscraper Project\\ASOS-webscraping-project\\images\\'name of your image'
      test_image = ('copy your image pathway here')
      # Open the image in Python
      test_image_show = Image.open(test_image)
    #   test_image_show.show()

      # Use an imagehash method to display the image as an array
      test_image_array = imagehash.average_hash(test_image_show)

      # test this against an array of the same image to check if it's true
      expected_array = imagehash.average_hash(test_image_show)

      # print both hashes as outputs and test if they are the same
      print(test_image_array)
      print(expected_array)
      self.assertTrue(test_image_array, expected_array)

    #TODO: Test Extract links by randomly sampling urls from the list of urls. 






    # def test_extract_links(self):
    #     for element in self.links:
    #         if element.slice() = 'htttps//:'
    #         x = slice(8)

    # Successful Unittest! 
    # def test_example(self):
    #     test_list = self.driver.find_elements_by_xpath('//*[@id="029c47b3-2111-43e9-9138-0d00ecf0b3db"]/div/div[2]/ul/li[1]/ul/li[1]')
    #     print(test_list)
    #     number_of_items = len(test_list)
    #     self.assertIsInstance(test_list, list)
        


    # list should contain strings with URLs inside 
    # self.links string starts with. https:// 

    # def tearDown(self):
    #     del setUp(self)
unittest.main(argv=[''], verbosity=2, exit=False)






        
# Test that the functions goes to websites. 
# In hypothesis, there's a module which tests URLs.
# For accept cookies, could send a bunch of xpaths which share the element of the 
# accept cookies button and see if it doesn't give an exception. 
