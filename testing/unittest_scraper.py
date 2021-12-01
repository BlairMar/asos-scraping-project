from io import TextIOWrapper
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

    # Successful Unittest ! 

    def test_scrape_and_save(self):
        # go to website 
        self.scraper.driver.get("https://www.asos.com")
        # run scrape_and_save method 
        sample_scrape = self.scraper.scrape_and_save() 
        # test if the output is a dictionary or tuple

        self.assertIsInstance(sample_scrape, TextIOWrapper)
    #    
    #   

    # Successful Unittest ! 

    def test_save_images(self):
        self.scraper.scrape_and_save()
        # Test if the image pathway is the same
        sample_image_pathway = self.scraper._save_image('Face + Body')
        print (sample_image_pathway)
        expected_output = 'images/Face + Body'
        self.assertEqual(sample_image_pathway, expected_output)

    # Successful Unittest ! 

    def test_save_to_json(self):
        # will need to get an output of a json file
        # then test if it is a valid json 
        # self.scraper._get_all_subcategory_hrefs()
        # runs main methods 
        test_information = self.scraper.scrape_and_save()
        print(type(test_information)) 
        # scrape_and_save returns a json formatted object. 
        # The type of a json is a TextIOWrapper therefore...
        self.assertIsInstance(test_information, TextIOWrapper)

        

        

    # Successful Unittest ! 

    def test_get_product_information(self):
        self.scraper.driver.get("https://www.asos.com/")    
        test_scrape = self.scraper.scrape_and_save()
        test_get_products = self.scraper._get_product_information(1)

        self.assertIsInstance(test_get_products, dict)


    # Successful Unittest ! 

    def test_get_details(self):
        self.scraper.scrape_and_save()
        test_dictionary = self.scraper._get_details()
        print(f'This is the test_dictionary: {test_dictionary}')
        self.assertIsInstance(test_dictionary, dict)
        

    
    def tearDown(self):
        self.scraper.driver.quit()

unittest.main(argv=[''], verbosity=2, exit=False)