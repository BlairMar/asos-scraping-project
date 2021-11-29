import unittest
from hypothesis.core import given
from ASOS_Scraper import AsosScraper
from selenium import webdriver 
import hypothesis.strategies as st 
import random
# import urllib.request

from PIL import Image
import hashlib
import time
import json



class ASOS_Webscraper_Tests(unittest.TestCase):
    # exec_path = r'C:\Users\EGuis\Webscraper_Project\ASOS-webscraping-project\chromedriver.exe'
    # base_URL =  "https://www.asos.com/men"
    
    
    def setUp(self):
        self.scraper = AsosScraper()
        time.sleep(5)  

        
    # Successful Unittest ! 

    def test_accept_cookies_button(self):
        click_accept_cookies = self.scraper.accept_cookies()
        self.assertTrue(click_accept_cookies)
    
    # Successful Unittest ! 

    def test_get_number_of_products(self):
        test_input = self.scraper._get_number_of_products()

        # Set the expected output in config.yaml 
        # Under the 'products_per_category:' field 

        expected_output = 3
        self.assertEqual(test_input, expected_output)

    # Successful Unittest ! 
    
    def test_scrape_category(self):
        self.scraper.driver.get("https://www.asos.com/women/")
        test_list = []
        test_scrape_list = self.scraper._scrape_category('//*[@id="chrome-sticky-header"]/div[2]/div[*]/nav/div/div/button[*]', test_list)
        print(test_scrape_list)
        self.assertIsInstance(test_scrape_list, list)
        # ^ Should return an empty list to be used in _get_all_subcategory_hrefs

    # Successful Unittest ! 
    
    def test_get_all_subcategory_hrefs(self):
        test_list = []
        self.scraper._scrape_category('//*[@id="chrome-sticky-header"]/div[2]/div[*]/nav/div/div/button[*]', test_list)
        test_subcategory_hrefs = self.scraper._get_all_subcategory_hrefs()
        print(test_subcategory_hrefs)
        self.assertIsInstance(test_subcategory_hrefs, list)

    
    # Successful Unittest ! 

    def test_extract_links(self):
        self.scraper.driver.get("https://www.asos.com/men/new-in/cat/?cid=27110&nlid=mw|new+in|new+products|view+all")
        hrefs_list = self.scraper._extract_links('//*[@id="plp"]/div/div/div[2]/div/div[1]/section/article/a', 'href')
        print(hrefs_list)
        test_hrefs_list = random.sample(hrefs_list,2)
        # test_hrefs_list = ['Miruna', 'James']
        value = bool
        for i in test_hrefs_list:
            try:
                self.scraper.driver.get(i)
            # return True
                print('Method is good')   
                value = True   
            except: 
                value = False
                print(value)
        
        self.assertTrue(value)
        

    # Successful Unittest ! 

    def test_set_s3_connection(self):
            test_connection = self.scraper.set_s3_connection()
            print(test_connection)
            self.assertIsInstance(test_connection, object)
    
    # Successful Unittest ! 

    def test_is_last_page(self):
        test_url = self.scraper.driver.get('https://www.asos.com/women/activewear/cat/?cid=26091&nlid=ww|sportswear|shop+by+product|view+all')
        # last_page = self.scraper.driver.find_elements_by_xpath('//*[@id="plp"]/div/div/div[2]/div/div[2]/progress').get_attribute('max')

        last_page = self.scraper._is_last_page()
        # assuming test_input under products_per_category = 3 
        self.assertFalse(last_page)

        

    # def test_save_images(self):
    #     sample_image_pathway = self.scraper._save_image('Face + Body')
    #     print (sample_image_pathway)
    #     expected_output = 'images/Face + Body'
    #     self.assertEqual(sample_image_pathway, expected_output)
    

    # def test_get_details(self):
    #     self.scraper.driver.get("https://www.asos.com/nike/nike-air-force-1-fontanka-trainers-in-sail-cream-and-multi/prd/24212993?colourwayid=60548206&cid=27108")
    #     test_dictionary = self.scraper._get_details()
    #     self.assertIsInstance(test_dictionary, dict)

    # def test_get_product_information(self):
    #     test_url = self.scraper.driver.get("https://www.asos.com/men/a-to-z-of-brands/topman/cat/?cid=29065&nlid=mw|topman|shop+by+product|view+all")
        
    #     test_dictionary = self.scraper._get_product_information(2)
    #     # Where 2 is the page number on the website 
    #     self.assertIsInstance(test_dictionary, dict)
    #     # self.scraper._get_number_of_products()
    #     # self.scraper._get_details()
    #     # self.scraper._get_product_information()
    
    
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

    # def test_save_to_json(self):
    #     # will need to get an output of a json file
    #     # then test if it is a valid json 
        
    #     URL = "https://www.asos.com/topman/topman-co-ord-skinny-check-jogger-trousers-in-black-and-white/prd/200391074?colourwayid=200391075&cid=27110"
    #     self.scraper.driver.get(URL)
    #     test_information = self.scraper.go_to_products() # runs main methods 
    #     # run the save_to_json method 
    #     test_json_data = self.scraper.save_to_json()

    #     try:
    #         json.loads(test_json_data)
    #         self.assertIsInstance(test_json_data, json)
    #     except ValueError as err:
    #         return False
    #     return True 
        

    
    def tearDown(self):
        self.scraper.driver.quit()

unittest.main(argv=[''], verbosity=2, exit=False)