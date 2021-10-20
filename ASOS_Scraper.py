from pprint import pprint
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import itertools

class AsosScraper:
     def __init__ (self, driver: webdriver.Chrome(), gender: str):
        self.root = "https://www.asos.com/"
        self.gender = gender
        URL = self.root + gender
        self.driver = driver 
        driver.get(URL)
        self.a = ActionChains(self.driver)  #object of ActionChains; it ads hover over functionality 
        self.links = [] # Initialize links, so if the user calls for extract_links inside other methods, it doesn't throw an error
       
     def extract_links(self, xpath: str): # given a common xpath, this method extracts the unique xpaths in a list and get the 'href' attribute for every unique xpath of an webelement
         xpaths_list = self.driver.find_elements_by_xpath(xpath) 
         self.links = []
         for item in xpaths_list:
            self.links.append(item.find_element_by_xpath('.//a').get_attribute('href'))
     
     def accept_cookies_button(self):
        time.sleep(4)
        click_accept_cookies = self.driver.find_element_by_xpath('//button[@class="g_k7vLm _2pw_U8N _2BVOQPV"]')
        click_accept_cookies.click()
     
     def choose_category(self):  #this method finds the second button (out of 12) from the category buttons top bar, and perform a hover over element function 
        category_button = self.driver.find_element_by_xpath('//*[@id="chrome-sticky-header"]/div[2]/div[2]/nav/div/div/button[2]')
        self.a.move_to_element(category_button).perform()  
        time.sleep(4)            #this will hover over the "New in" category and show the 'New in' subcategories

     def get_submenu_product_list(self): #this method uses the "extract_links" method to access the first href (self.links[0]) in the "New in" subcategories list, which is "New in -> View all "
         self.extract_links('//*[@id="029c47b3-2111-43e9-9138-0d00ecf0b3db"]/div/div[2]/ul/li[1]/ul/li[*]')
         self.driver.get(self.links[0])
     
     def get_product_list_urls(self): #this method uses the "extract_links" method to extract the hrefs for every product in the 'New in/View all' 
        self.extract_links('//*[@id="plp"]/div/div/div[2]/div/div[1]/section[1]/article')
        self.product_urls = self.links #save the list with hrefs in another variable that will be reffered to in the following methods
    
     def product_information(self):
            ''' 
    #TODO: Add image scraping functionality and create folder to add them to. Naming files appropriately too.
    A function to iterate through the product URL's of a webpage,
    scrape product data and then append the data to a dictionary.
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
        
               print(self.product_information_dict)
     
    

product_search = AsosScraper(webdriver.Chrome(),'men')
product_search.accept_cookies_button()
product_search.choose_category()
product_search.get_submenu_product_list()
product_search.get_product_list_urls()
product_search.product_information()