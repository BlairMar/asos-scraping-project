import pprint
import os
import time
import json
import itertools
import urllib.request
import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from tqdm import tqdm

class AsosScraper:
    def __init__(self,driver):
        self.root = "https://www.asos.com/"
        self.gender_dict = {'men':2,'women':1}
        # self.gender_dict = {'women':1}
        # self.gender = gender
        # URL = self.root + self.gender
        # self.driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME)
        self.driver = driver
        driver.get(self.root)
        self.driver.get(self.root)
        # object of ActionChains; it ads hover over functionality
        self.a = ActionChains(self.driver)
        self.links = []  # Initialize links, so if the user calls for extract_links inside other methods, it doesn't throw an error
        
    def get_gender_hrefs(self):
        self.all_main_categories_hrefs = []
        for key,value in self.gender_dict.items():
            self.driver.get(self.root + f'{key}')
            # find_element_by_xpath(f'//*[@id="{key}-floor"]').click()
            self._choose_category(f'//*[@id="chrome-sticky-header"]/div[2]/div[{value}]/nav/div/div/button[*]')
            # print(self.gender_hrefs)
            self.all_main_categories_hrefs.extend(self.gender_hrefs)
        print(self.all_main_categories_hrefs)

    def _choose_category(self,xpath):
        self.gender_hrefs = [] #href links to be scraped
        self.category_list = ['Clothing', 'Shoes', 'Accessories', 'Sportswear', 'Face + Body']
        category_list_to_dict = [] #see below, this list will contain the category name, the number of the category button and the corresponding webelement (button) 
        main_category_elements = self.driver.find_elements_by_xpath(xpath)
        
        for element in main_category_elements:
            main_category_heading = element.find_element_by_css_selector('span span').text
            
            if main_category_heading in self.category_list:  #if any item in main_category_heading is foung in self.category_list, then append everything below to a list
                category_list_to_dict.append(main_category_heading) # the name of the subcategory corresponding to self.category_list
                category_list_to_dict.append(int(element.get_attribute('data-index')) + 1) # -> the number of the button corresponding to the category; to be used on line 51 ({elements[0]})
                category_list_to_dict.append(element) # -> category button to hover over
        
        #create a dictionary out of the list, key = main_category_heading, value1 = number of button, value2 = webelement (button) to hover over 
        category_dict = {category_list_to_dict[i]:[category_list_to_dict[i + 1],category_list_to_dict[i + 2]] for i in range(0, len(category_list_to_dict), 3)}  
        
        #category_dict -  How it is created - category dict list = ['clothing, 4, <webelement>, 'Shoes', 5, <webelement>, 'Accessories', 6, <webelement> ...]
        #for i in range (0,len(category_list_to_dict),3) where 3 is the step -> category_list_to_dict[i] = key, [category_list_to_dict[i + 1] = value 1,category_list_to_dict[i + 2]] - value 2
        
        # {
        #   'Clothing': [4, <selenium.webdriver.remote...5552")>], 
        #   'Shoes': [5, <selenium.webdriver.remote...354c1")>], 
        #   'Accessories': [6, <selenium.webdriver.remote...b302")>], 
        #   'Sportswear': [8, <selenium.webdriver.remote...40fa")>], 
        #   'Face + Body': [9, <selenium.webdriver.remote...ba7d9")>]
        # }
        
        subcategory_elements_list = [] #this list has nested lists containing the webelements corresponding to the subcategories insidde one main category : [[clothing subactegories webelements],[shoes subcategories webelements], ...[face+body subcategry webelements]]
        for i, (key, elements) in enumerate(category_dict.items()): #enumerate through the category_dict -> i = 0, key0, value0.0,value0.1; i = 1,key1, value1.0, value1.1 etc
            elements[1].click() #move to value index 1 (second value of the key = button element) of every key (category) snd hover over 
            time.sleep(3)

            subcategory_elements_list.append(self.driver.find_elements_by_xpath(f'//div[{elements[0]}]/div/div[2]/ul/li[1]/ul/li/a')) #append every list with subcategories webelements, see how list will look like in the comment on line 51         
            for element in subcategory_elements_list[i]:  #for every element inside every nested list, extract the href only for the webelements containg the 'view all' or 'new in' text
                if element.text == 'View all':
                    self.gender_hrefs.append(element.get_attribute('href'))
                    break
                elif element.text == 'New in': 
                    temp = element
                    # self.links.append(element.get_attribute('href'))   #append the desired hrefs to the self.links list initialised at the start 
                    
            else:
                self.gender_hrefs.append(temp.get_attribute('href'))
                
           
        return self.gender_hrefs

product_search = AsosScraper(webdriver.Chrome())
product_search.get_gender_hrefs()
product_search.driver.quit()
