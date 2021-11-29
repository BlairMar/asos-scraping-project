import unittest
from hypothesis.core import given
from selenium.webdriver.android.webdriver import WebDriver
from ASOS_Webscraper import AsosScraper
from selenium import webdriver 
import hypothesis.strategies as st 
import random
# import urllib.request
from input_file import User_input 
from PIL import Image
import hashlib
import time
import json


class ASOS_Webscraper_Tests(unittest.TestCase):
    # exec_path = r'C:\Users\EGuis\Webscraper_Project\ASOS-webscraping-project\chromedriver.exe'
    # base_URL =  "https://www.asos.com/men"
    
    
    def setUp(self):
        self.scraper = AsosScraper()
        self.instance_choices = User_input()
        time.sleep(5)  

        
    # # Successful Unittest ! 
    # def test_click_buttons(self):
    #     click_accept_cookies = self.scraper.click_buttons('//*[@id="chrome-header"]/header/div[1]/div/div/button', 1)
    #     self.assertTrue(click_accept_cookies)
    

    

    # # Sucessful Unittest ! 

    # def test_extract_links(self):
    #     self.scraper.driver.get("https://www.asos.com/men/new-in/cat/?cid=27110&nlid=mw|new+in|new+products|view+all")
    #     hrefs_list = self.scraper._extract_links('//*[@id="plp"]/div/div/div[2]/div/div[1]/section[1]/article')
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
    #     assert True
        

    # def test_load_more_products(self):
    #     # goes to the url of the page 
    #     self.scraper.driver.get("https://www.asos.com/men/new-in/cat/?cid=27110&nlid=mw|new+in|new+products|view+all")
        
    #     # runs load_more_products on the page. Defaults to 1 for section 1 
    #     actual_value = self.scraper._extract_links('//*[@id="plp"]/div/div/div[2]/div')
    #     print(actual_value)
    #     expected_value = str
    #     # print(productlist)
    #     # self.assertIsInstance(productlist,int)
    #     self.assertEqual(actual_value,expected_value)
       

    
    
    # def test_image_output(self):
    # #   # copy your image pathway inside these brackets. 
    # #   # use an r string for backlashes or use double backlashes to avoid an error 
    # #   # example: 'C:\\Users\\WR\\Webscraper Project\\ASOS-webscraping-project\\images\\'name of your image'
    #   test_image = (r'C:\Users\EGuis\Webscraper_Project\ASOS-webscraping-project\images\Test_Image.webp')
    # #   # Open the image in Python
    # #   test_image_show = Image.open(test_image)
    # # #   test_image_show.show()
    # #   self.driver.find_element_by_xpath('//*[@id="chrome-app-container"]/section[2]/div/a/div[1]/picture/source')
    # #   self.get('srcsecret')
    # #   self.scraper.get('https://www.asos.com/mad-beauty/star-wars-stormtrooper-soap-on-a-rope/prd/201118899?colourwayid=201118901&cid=27110')

    #   actual_value = hashlib.md5(test_image.tobytes()).hexdigest()
    # #   Use an imagehash method to display the image as an array
    # #   test_image_array = imagehash.average_hash(test_image_show)

    # #   test this against an array of the same image to check if it's true
    #   expected_array = '61dd3ac27fb79ae115f9e622ab88e903'

    # #   print both hashes as outputs and test if they are the same
    #   print(actual_value)
    #   print(expected_array)
    #   self.assertEqual(actual_value, expected_array)

    #   print(type(actual_value))

    def test_save_to_json(self):
        # will need to get an output of a json file
        # then test if it is a valid json 
        
        URL = "https://www.asos.com/topman/topman-co-ord-skinny-check-jogger-trousers-in-black-and-white/prd/200391074?colourwayid=200391075&cid=27110"
        self.scraper.driver.get(URL)
        test_information = self.scraper.go_to_products() # runs main methods 
        # run the save_to_json method 
        test_json_data = self.scraper.save_to_json()

        try:
            json.loads(test_json_data)
            self.assertIsInstance(test_json_data, json)
        except ValueError as err:
            return False
        return True 
        
           
    
           

        
    
        
    


    
    def tearDown(self):
        self.scraper.driver.quit()

unittest.main(argv=[''], verbosity=2, exit=False)