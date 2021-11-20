import os
import time
import json
import itertools
import urllib.request
import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from tqdm import tqdm
import boto3
import tempfile
import shutil


# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
s3_client = boto3.client('s3')
class AsosScraper:
     def __init__(self, driver):
        self.root = "https://www.asos.com/"
        self.gender_dict = {'men':2,'women':1}
        # self.driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME)
        self.driver = driver
        driver.get(self.root)
        self.a = ActionChains(self.driver) # object of ActionChains; it ads hover over functionality
        self.links = []  # Initialize links, so if the user calls for extract_links inside other methods, it doesn't throw an error
        self.all_categories_hrefs = []
     # given a common xpath, this method extracts the unique xpaths in a list and get the 'href' attribute for every unique xpath of an webelement
    
     def _get_gender_hrefs(self):
        for key,value in self.gender_dict.items():
            self.driver.get(self.root + f'{key}')
            self._choose_category(f'//*[@id="chrome-sticky-header"]/div[2]/div[{value}]/nav/div/div/button[*]')
            self.all_categories_hrefs.extend(self.gender_hrefs)
        return self.all_categories_hrefs
    
     def primary_method(self):
         self._get_gender_hrefs()
         for href in self.all_categories_hrefs:
            self.driver.get(href)
            self._load_more_products()
            self._go_to_products()
            time.sleep(5)
    
     def _extract_links(self, xpath: str):
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
     
     def _choose_category(self,xpath:str):
        self.gender_hrefs = [] #href links to be scraped
        self.category_list = ['Clothing', 'Shoes', 'Accessories', 'Sportswear', 'Face + Body']
        category_list_to_dict = [] #see below, this list will contain the category name, the number of the category button and the corresponding webelement (button) 
        main_category_elements = self.driver.find_elements_by_xpath(xpath)
        
        for element in main_category_elements:
            main_category_heading = element.find_element_by_css_selector('span span').text
            
            if main_category_heading in self.category_list:  
                category_list_to_dict.append(main_category_heading) 
                category_list_to_dict.append(int(element.get_attribute('data-index')) + 1) 
                category_list_to_dict.append(element) 
        
       
        category_dict = {category_list_to_dict[i]:[category_list_to_dict[i + 1],category_list_to_dict[i + 2]] for i in range(0, len(category_list_to_dict), 3)}  
        subcategory_elements_list = [] 
        for i, (key, elements) in enumerate(category_dict.items()): 
            elements[1].click()  
            time.sleep(3)

            subcategory_elements_list.append(self.driver.find_elements_by_xpath(f'//div[{elements[0]}]/div/div[2]/ul/li[1]/ul/li/a'))          
            for element in subcategory_elements_list[i]:  
                if element.text == 'View all':
                    self.gender_hrefs.append(element.get_attribute('href'))
                    break
                elif element.text == 'New in': 
                    temp = element        
            else:
                self.gender_hrefs.append(temp.get_attribute('href'))        
        return self.gender_hrefs
 
     # this method will extract the products' hrefs products from (page_number = 4) pages
     def _load_more_products(self): 
         self.click_buttons('//*[@id="plp"]/div/div/div[2]/div/a', load_more)
         sections_xpaths_list = []
         for _ in range(1, page_number):
            sections_xpaths_list.append(f'//*[@id="plp"]/div/div/div[2]/div/div[1]/section[{_}]/article')  
         
         list_all_products = []
         for section_xpath in sections_xpaths_list:# for every section(page with 72 products) use the "extract_links" method to extract the hrefs for every product on the page
             self._extract_links(section_xpath)
             list_all_products += self.links  #self.links will extract 72 hrefs for every section_xpath and will be added to the list_all_products
         self.product_urls = list_all_products # save the list with hrefs in another variable that will be reffered to in the following methods
         time.sleep(3)

     def _go_to_products(self):
         n = 3
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
            time.sleep(3)
            self._get_details()
            time.sleep(3)
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
         self.xpath_src_list = self.driver.find_elements_by_xpath('//*[@id="product-gallery"]/div[1]/div[2]/div[*]/img')
         self.src_list = []                                        
         for xpath_src in self.xpath_src_list:
            self.src_list.append(xpath_src.get_attribute('src'))
         
         with tempfile.TemporaryDirectory() as temp_dir:
            for i,src in enumerate(self.src_list[:-1],1):   
                urllib.request.urlretrieve(src, f'{temp_dir}/image_{i}.jpg')
                s3_client.upload_file(f'{temp_dir}/image_{i}.jpg','asosscraperbucket',
                f'images/{sub_category_name}/{sub_category_name}-product{self.product_number}.{i}.jpg')

         if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
         return self.src_list

     def _save_to_json(self, product_dict_list: dict, sub_category_name: str): 
         with open(f'json_files\{sub_category_name}_details.json', mode='a+') as f:
             json.dump(product_dict_list, f, indent=4) #'indent = x' to format output in json file, visually better
             f.write('\n')

         with tempfile.TemporaryDirectory() as temp_dir1:
            with open(f'{temp_dir1}/{sub_category_name}_details.json', mode='a+') as f:
                json.dump(product_dict_list, f, indent=4) #'indent = x' to format output in json file, visually better
                f.write('\n')
                f.flush()
                time.sleep(3)
                s3_client.upload_file(f'{temp_dir1}/{sub_category_name}_details.json', 'asosscraperbucket', f'json_files/{sub_category_name}_details.json')
               
         if os.path.exists(temp_dir1):
                shutil.rmtree(temp_dir1)

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
    product_search = AsosScraper(webdriver.Chrome())
    product_search.click_buttons('//*[@id="chrome-header"]/header/div[1]/div/div/button', 1) #this xpath is for accepting the cookies                         
    product_search.primary_method()
    product_search.driver.quit()
    

