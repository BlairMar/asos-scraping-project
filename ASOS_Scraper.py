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
     def __init__(self, driver, gender: str):
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
        #  print(len(self.links))
         return self.links
        #  print(self.links)
     

     def click_buttons(self, button_xpath, n_clicks: int ): # n_clicks is the number of clicks 
        for i in range(1, n_clicks + 1):
            button = self.driver.find_element_by_xpath(button_xpath)
            button.click()
            i += 1
            time.sleep(3)
        return True
        
     # this method finds the second button (out of 12) from the category buttons top bar, and perform a hover over element function
     def choose_category(self, category_xpath:str): #category_xpath: str
        category_button = self.driver.find_element_by_xpath(category_xpath)
        self.a.move_to_element(category_button).perform()
        # this will hover over the "New in" category and show the 'New in' subcategories
        time.sleep(4)

     # this method uses the "extract_links" method to access the first href (self.links[0]) in the "New in" subcategories list, which is "New in -> View all "
     def go_to_products_page(self, subcategory_xpath, index: int):
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
            #  return len(list_all_products)
        
         print(len(list_all_products))
         self.product_urls = list_all_products # save the list with hrefs in another variable that will be reffered to in the following methods
        #  return self.product_urls
         return len(list_all_products)
     
       
     def go_to_products(self):
        # url_counter = 0
         n = 10
         self.product_dict_list = {}
         self.sub_category_name = self.driver.find_element_by_xpath(
             '//*[@id="category-banner-wrapper"]/div/h1').text.lower().replace(" ", "-").replace(":","").replace("'","")
        
         for nr, url in tqdm(itertools.islice(enumerate(self.product_urls,1),n)): 
            self.product_number = nr
            self.driver.get(url)

            self.product_information_dict = {f'{self.sub_category_name}-product-{self.product_number}': 
                                              {'Product Name': [],
                                               'Price': [],
                                               'Product Details' : [],
                                               'Product Code': [],
                                               'Colour': []
                                               }
                                             }
            
            self._get_details()
            self._download_images(self.sub_category_name)
            self.product_dict_list.update(self.product_information_dict)
         self._save_to_json(self.product_dict_list, self.sub_category_name)
          
     def _get_details(self):
        try: #find details info
            for key in xpath_dict:
                if key == 'Product Details':
                    details_container = self.driver.find_elements_by_xpath(xpath_dict[key])
                    for detail in details_container:
                        self.product_information_dict[f'{self.sub_category_name}-product-{self.product_number}'][key].append(detail.text)

                else:
                    dict_key = self.driver.find_element_by_xpath(xpath_dict[key])
                    self.product_information_dict[f'{self.sub_category_name}-product-{self.product_number}'][key].append(dict_key.text)

        except:
            self.product_information_dict[f'{self.sub_category_name}-product-{self.product_number}'][key].append('No information found')
        
        return self.product_information_dict

     def _download_images(self, sub_category_name: str):
         
         if not os.path.exists(f'images\{sub_category_name}'): #if there is no existing directory called "images", create one
            os.makedirs(f'images\{sub_category_name}')

         self.xpath_src_list = self.driver.find_elements_by_xpath('//*[@id="product-gallery"]/div[1]/div[2]/div[*]/img')
         self.src_list = []                                        
         for xpath_src in self.xpath_src_list:
            self.src_list.append(xpath_src.get_attribute('src'))
        
         for i,src in enumerate(self.src_list[:-1],1):   
            urllib.request.urlretrieve(src, f'images\{sub_category_name}\{sub_category_name}-product{self.product_number}.{i}.jpg')

     def _save_to_json(self, product_dict_list: dict, sub_category_name: str):
         if not os.path.exists('json_files'): 
            os.makedirs('json_files')
        #with open('JSON-files\new-in\view-all.json', mode='a+') as f: 
         with open(f'json_files\{sub_category_name}_details.json', mode='a+') as f:
             json.dump(product_dict_list, f, indent=4) #'indent = x' to format output in json file, visually better
             f.write('\n')

new_in_dict = {'subcategory_xpath': '//*[@id="029c47b3-2111-43e9-9138-0d00ecf0b3db"]/div/div[2]/ul/li[1]/ul/li[*]',
 'index': 1, 'subcategory_name': str}

names_list = []
for subcategory_index, name1 in zip(range(len(names_list)),names_list):
    new_in_dict['index'] =  subcategory_index
    new_in_dict['subcategory_name'] = name1

xpath_dict = {
                'Product Name': '//*[@id="aside-content"]/div[1]/h1',
                'Price': '//*[@id="product-price"]/div/span[2]/span[4]/span[1]',
                'Product Details' : '//*[@id="product-details-container"]/div[1]/div/ul/li',
                'Product Code': '/html/body/div[2]/div/main/div[2]/section[2]/div/div/div/div[2]/div[1]/p',
                'Colour': '//*[@id="product-colour"]/section/div/div/span'
                }  #use this dictionary inside the product_information method

load_more = 3 #how many time to click the load more button
page_number = load_more + 2 #page number is the range of pages we want to display - range (1,pagenumber = 5) means that we will display 4 pages

if __name__ == '__main__':
    product_search = AsosScraper(webdriver.Chrome(),'men')
    product_search.click_buttons('//button[@class="g_k7vLm _2pw_U8N _2BVOQPV"]', 1) #this xpath is for accepting the cookies
    product_search.choose_category('//*[@id="chrome-sticky-header"]/div[2]/div[2]/nav/div/div/button[2]')
    # product_search.extract_links('//*[@id="029c47b3-2111-43e9-9138-0d00ecf0b3db"]/div/div[2]/ul/li[1]/ul/li[*]')
    
    # for subcategory_index in range(1,3):
    #     new_in_dict['index'] =  subcategory_index
    product_search.go_to_products_page(new_in_dict['subcategory_xpath'], new_in_dict['index']) #, dict['product_urls_xpath'])
    product_search.click_buttons('//*[@id="plp"]/div/div/div[2]/div/a', load_more) #this xpath is used to click the 'Load more' button
    product_search.load_more_products()
    product_search.go_to_products()
    # AsosScraper.driver.quit()
    

