from pprint import pprint
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import itertools
import urllib.request


class AsosScraper:
     def __init__(self, driver: webdriver.Chrome(), gender: str):
        self.root = "https://www.asos.com/"
        self.gender = gender
        URL = self.root + gender
        self.driver = driver
        driver.get(URL)
        # object of ActionChains; it ads hover over functionality
        self.a = ActionChains(self.driver)
        self.links = []  # Initialize links, so if the user calls for extract_links inside other methods, it doesn't throw an error
    
     # given a common xpath, this method extracts the unique xpaths in a list and get the 'href' attribute for every unique xpath of an webelement
     def extract_links(self, xpath: str):
         xpaths_list = self.driver.find_elements_by_xpath(xpath)
         self.links = []
         for item in xpaths_list:
            self.links.append(item.find_element_by_xpath(
                './/a').get_attribute('href'))

     def click_buttons(self, button_xpath, n_clicks: int ): # n_clicks is the number of clicks 
        for i in range(1, n_clicks + 1):
            button = self.driver.find_element_by_xpath(button_xpath)
            button.click()
            i += 1
            time.sleep(3)
        
     # this method finds the second button (out of 12) from the category buttons top bar, and perform a hover over element function
     def choose_category(self, category_xpath:str): #category_xpath: str
        category_button = self.driver.find_element_by_xpath(category_xpath)
        self.a.move_to_element(category_button).perform()
        # this will hover over the "New in" category and show the 'New in' subcategories
        time.sleep(4)

     # this method uses the "extract_links" method to access the first href (self.links[0]) in the "New in" subcategories list, which is "New in -> View all "
     def go_to_product(self, subcategory_xpath, index: int):
         self.extract_links(subcategory_xpath)  
         self.driver.get(self.links[index])
            
     # this method will extract the products' hrefs products from (pagen_number = 4) pages
     def load_more_products(self): 
         sections_xpaths_list = []
         for _ in range(1, page_number):
            sections_xpaths_list.append(f'//*[@id="plp"]/div/div/div[2]/div/div[1]/section[{_}]/article')  
         
         list_all_products = []
         for section_xpath in sections_xpaths_list:# for every section(page with 72 products) use the "extract_links" method to extract the hrefs for every product on the page
             self.extract_links(section_xpath)
             list_all_products += self.links  #self.links will extract 72 hrefs for every section_xpath and will be added to the list_all_products
        
         print(len(list_all_products))
         self.product_urls = list_all_products # save the list with hrefs in another variable that will be reffered to in the following methods


     def product_information(self, xpath_dict):
            '''
    # TODO: Add image scraping functionality and create folder to add them to. Naming files appropriately too.
    A function to iterate through the product URL's of a webpage,
    scrape product data and then append the data to a dictionary.
    Attributes:
        xpath_dict : a dictionary containing details to be scraped and relevant xpath
        product_information_dict : empty dictionary to have scraped details appended to
    Returns:
        Data organised into a dictionary for every product visited
    '''
            url_counter = 0
            for url in self.product_urls:  # TODO: use enumerate
               self.driver.get(url)
               url_counter += 1
               if url_counter == 4: #breaks after 3 items just for testing purposes
                 break

               self.product_information_dict = {
                                f'Product{url_counter}': {
            'Product Name': [],
            'Price': [],
            'Product Details' : [],
            'Product Code': [],
            'Colour': []
            }
            }
               try: #find details info
                    for key in xpath_dict:
                       if key == 'Product Details':
                           details_container = self.driver.find_elements_by_xpath(xpath_dict[key])
                           for detail in details_container:
                            self.product_information_dict[f'Product{url_counter}'][key].append(detail.text)

                       else:
                          dict_key = self.driver.find_element_by_xpath(xpath_dict[key])
                          self.product_information_dict[f'Product{url_counter}'][key].append(dict_key.text)

               except:
                    self.product_information_dict[f'Product{url_counter}'][key].append('No information found')
                   
               #download the each product images to the images folder        
               self.xpath_src_list = self.driver.find_elements_by_xpath('//*[@id="product-gallery"]/div[1]/div[2]/div[*]/img')
               self.src_list = []                                        
               for xpath_src in self.xpath_src_list:
                   self.src_list.append(xpath_src.get_attribute('src'))
        
               for i,src in enumerate(self.src_list[:-1]):   
                   urllib.request.urlretrieve(src, f"images\{self.gender}_Product{url_counter}.{i}.jpg")

               print(self.product_information_dict)
     
    
New_in_dict = {'subcategory_xpath': '//*[@id="029c47b3-2111-43e9-9138-0d00ecf0b3db"]/div/div[2]/ul/li[1]/ul/li[*]',
 'index': 0}

xpath_dict = {
                'Product Name': '//*[@id="aside-content"]/div[1]/h1',
                'Price': '//*[@id="product-price"]/div/span[2]/span[4]/span[1]',
                'Product Details' : '//*[@id="product-details-container"]/div[1]/div/ul/li',
                'Product Code': '/html/body/div[2]/div/main/div[2]/section[2]/div/div/div/div[2]/div[1]/p',
                'Colour': '//*[@id="product-colour"]/section/div/div/span'
                }  #use this dictionary inside the product_information method

load_more = 3 #how many time to click the load more button
page_number = load_more + 2 #page number is the range of pages we want to display - range (1,pagenumber = 5) means that we will display 4 pages

product_search = AsosScraper(webdriver.Chrome(),'men')
product_search.click_buttons('//button[@class="g_k7vLm _2pw_U8N _2BVOQPV"]', 1) #this xpath is for accepting the cookies
product_search.nice_method()
product_search.choose_category('//*[@id="chrome-sticky-header"]/div[2]/div[2]/nav/div/div/button[2]')
product_search.go_to_product(New_in_dict['subcategory_xpath'], New_in_dict['index']) #, dict['product_urls_xpath'])
product_search.click_buttons('//*[@id="plp"]/div/div/div[2]/div/a', load_more) #this xpath is used to click the 'Load more' button
product_search.load_more_products()
# product_search.product_information(xpath_dict)

