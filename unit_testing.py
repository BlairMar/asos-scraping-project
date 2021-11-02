import unittest
from hypothesis.core import given
from selenium.webdriver.android.webdriver import WebDriver
from ASOS_Scraper import AsosScraper 
from selenium import webdriver 
import hypothesis.strategies as st 
import random
import urllib.request
from PIL import Image
import hashlib


class ASOS_Webscraper_Tests(unittest.TestCase):
    exec_path = r'C:\Users\Miruna\Desktop\Web Scraper ASOS\ASOS-webscraping-project\chromedriver.exe'
    base_URL =  "https://www.asos.com/men"
    
    
    def setUp(self):
        self.scraper = AsosScraper(webdriver.Chrome(), "men")        
        
    # def test_click_buttons(self):
    #     click_accept_cookies = self.scraper.click_buttons('//button[@class="g_k7vLm _2pw_U8N _2BVOQPV"]', 1)
    #     self.assertTrue(click_accept_cookies)

    # def test_ASOS_SCRAPER(self):
    #     driver = webdriver.Chrome(executable_path= self.exec_path)
    #     driver.get(self.base_URL)
    #     mp = AsosScraper(driver)
    #     mp.test_title()

    # def test_extract_links(self):
    #     self.scraper.driver.get("https://www.asos.com/men/new-in/cat/?cid=27110&nlid=mw|new+in|new+products|view+all")
    #     hrefs_list = self.scraper.extract_links('//*[@id="plp"]/div/div/div[2]/div/div[1]/section[1]/article')
    #     test_hrefs_list = random.sample(hrefs_list,2)
    #     # test_hrefs_list = ['Miruna', 'James']
    #     value = bool
    #     for i in test_hrefs_list:
    #         try:
    #             self.scraper.driver.get(i)
    #         # return True
    #         # print('Method is good')   
    #             value = True   
    #         except: 
    #             value = False
        
    #     self.assertTrue(value)
    #     # assert True
        

    # def test_load_more_products(self):
    #     # goes to the url of the page 
    #     self.scraper.driver.get("https://www.asos.com/men/new-in/cat/?cid=27110&nlid=mw|new+in|new+products|view+all")
    #     # runs load_more_products on the page. Defaults to 1 for section 1 
    #     actual_value = self.scraper.load_more_products()
    #     expected_value = 72
    #     # print(productlist)
    #     # self.assertIsInstance(productlist,int)
    #     self.assertEqual(actual_value,expected_value)

    
    
    def test_image_output(self):
      # copy your image pathway inside these brackets. 
      # use an r string for backlashes or use double backlashes to avoid an error 
      # example: 'C:\\Users\\WR\\Webscraper Project\\ASOS-webscraping-project\\images\\'name of your image'
      test_image = (r'C:\Users\Miruna\Desktop\Web Scraper ASOS\ASOS-webscraping-project\images\men_Product1.0.jpg')
      # Open the image in Python
      test_image_show = Image.open(test_image)
    #   test_image_show.show()
     
      self.scraper.get('https://www.asos.com/mad-beauty/star-wars-stormtrooper-soap-on-a-rope/prd/201118899?colourwayid=201118901&cid=27110')

      actual_value = hashlib.md5(test_image_show.tobytes()).hexdigest()
      # Use an imagehash method to display the image as an array
      # test_image_array = imagehash.average_hash(test_image_show)

      # test this against an array of the same image to check if it's true
      # expected_array = '61dd3ac27fb79ae115f9e622ab88e903'

      # print both hashes as outputs and test if they are the same
      # print(test_image_array)
      # print(expected_array)
      # self.assertEqual(actual_value, expected_array)

      print(type(actual_value))


  

    # def tearDown(self):
    #     del setUp(self)

unittest.main(argv=[''], verbosity=2, exit=False)






        
# Test that the functions goes to websites. 
# In hypothesis, there's a module which tests URLs.
# For accept cookies, could send a bunch of xpaths which share the element of the 
# accept cookies button and see if it doesn't give an exception.