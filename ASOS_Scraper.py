from pprint import pprint
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import itertools
import json

class AsosScraper:
     def __init__ (self, driver: webdriver.Chrome(), gender: str):
        self.root = "https://www.asos.com/"
        self.gender = gender
        URL = self.root + gender
        self.driver = driver 
        driver.get(URL)
        self.a = ActionChains(self.driver)  #object of ActionChains; it ads hover over functionality 
        self.product_dict_list = {}

     def accept_cookies_button(self):
        time.sleep(1)
        click_accept_cookies = self.driver.find_element_by_xpath('//button[@class="g_k7vLm _2pw_U8N _2BVOQPV"]')
        click_accept_cookies.click()
     
     def choose_category(self):     

        category_button = self.driver.find_element_by_xpath('//*[@id="chrome-sticky-header"]/div[2]/div[2]/nav/div/div/button[2]')
        self.a.move_to_element(category_button).perform()  
        time.sleep(1)

     def get_submenu_product_list(self):     #show submenu and get a list with xpaths for evry subcategory
        self.submenu_xpath_product_list = self.driver.find_elements_by_xpath('//*[@id="029c47b3-2111-43e9-9138-0d00ecf0b3db"]/div/div[2]/ul/li[1]/ul/li[*]')
        self.new_list = []  
        for item in self.submenu_xpath_product_list: #create a new list witht the 'href's for every webelement in the above list 
            link = item.find_element_by_xpath('.//a').get_attribute('href')
            self.new_list.append(link)
            
     def choose_subcategory(self):
        self.driver.get(self.new_list[0])  #goes to Men/New in/View All, where self.new_list contains the 'href's for 
                                           #all the subcategories in Men/New in and self.new_list[0] = 'View all', the first element of the list
            # for item in self.new_list:
            #    self.driver.get(item)                                  

     def get_product_list_urls(self):
        product_container = self.driver.find_element_by_xpath('//*[@id="plp"]/div/div/div[2]/div/div[1]/section[1]') 
        self.product_list = product_container.find_elements_by_xpath('./article')
        self.product_urls = []
        for item1 in self.product_list:
            link1 = item1.find_element_by_xpath('.//a').get_attribute('href')
            self.product_urls.append(link1)

   #   def go_to_product(self):
   #      n = 3 #n tells how many prodducts we want to look at
   #      #need an empty dictionary for the details 
   #      for product in itertools.islice(self.product_urls,n):
   #          self.driver.get(product)
         
     def product_information(self):
        ''' 
         Attributes:
         xpath_dict : a dictionary containing details to be scraped and relevant xpath
         product_information_dict : empty dictionary to have scraped details appended to
         Returns:
         Data organised into a dictionary for every product visited
        '''
        
        self.xpath_dict = {
                'Product Name' : '//*[@id="aside-content"]/div[1]/h1', 
                'Price' : '//*[@id="product-price"]/div/span[2]/span[4]/span[1]', 
                # 'Product Details' : list, 
                'Product Code' : '/html/body/div[2]/div/main/div[2]/section[2]/div/div/div/div[2]/div[1]/p', 
                'Colour' : '//*[@id="product-colour"]/section/div/div/span' 
                }
        url_counter = 0
        for url in self.product_urls: #TODO: use enumerate
               self.driver.get(url)
               url_counter += 1
               self.product_information_dict = {
                                    f'Product{url_counter}':{
            'Product Name' : [], 
            'Price' : [], 
            # 'Product Details' : [], 
            'Product Code' : [], 
            'Colour' : []
            }
            }
               try: #find details info
                  for key in self.xpath_dict:
                   dict_key = self.driver.find_element_by_xpath(self.xpath_dict[key])
                   self.product_information_dict[f'Product{url_counter}'][key].append(dict_key.text)
               except:
                   self.product_information_dict[f'Product{url_counter}'][key].append('No information found')
        
               if url_counter == 4: #breaks after 3 items just for testing purposes
                 break
               self.product_dict_list.update(self.product_information_dict)
               #print(self.product_information_dict)
        
        print(self.product_dict_list)
        return(self.product_dict_list)
     
     
     
     def save_to_json(self):
       #with open('JSON-files\new-in\view-all.json', mode='a+') as f: 
        with open('JSON_details.json', mode='a+') as f:
           json.dump(self.product_dict_list, f, indent=4) #'indent = x' to format output in json file, visually better
           f.write('\n')
         #TODO:# Make function more generalised (i.e reusable)
         

product_search = AsosScraper(webdriver.Chrome(),'men')
product_search.accept_cookies_button()
product_search.choose_category()
product_search.get_submenu_product_list()
product_search.choose_subcategory()
product_search.get_product_list_urls()
product_search.product_information()
product_search.save_to_json()