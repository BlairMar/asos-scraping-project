import os
import time
import json
import itertools
from typing import Counter, NoReturn
import urllib.request
import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.webdriver import WebDriver
from tqdm import tqdm
import boto3
import tempfile
import shutil
from input_file import UserInput

class AsosScraper:
    
    xpath_dict = {
                'Product Name': '//*[@id="aside-content"]/div[1]/h1',
                'Price': '//*[@id="product-price"]/div/span[2]/span[4]/span[1]',
                'Product Details' : '//*[@id="product-details-container"]/div[1]/div/ul/li',
                'Product Code': '//*[@id="product-details-container"]/div[2]/div[1]/p',                                   
                'Colour': '//*[@id="product-colour"]/section/div/div/span'    
                }  #use this dictionary inside the product_information method

    accept_cookies = "//button[@data-testid ='close-button']"
     
    def __init__(self):
        self.root = "https://www.asos.com/"
        self.driver = webdriver.Chrome()
        # self.driver = webdriver.Remote("http://localhost:4444/wd/hub", DesiredCapabilities.CHROME)
        self.driver.get(self.root)
        self.a = ActionChains(self.driver) # object of ActionChains; it ads hover over functionality
        self.links = []  # Initialize links, so if the user calls for extract_links inside other methods, it doesn't throw an error
        self.all_categories_hrefs = []
        self.config = UserInput()
        self.load_more = self.config.products_per_category // 72

    
    # def get_categories_options_from_ASOS(self):
    #     self.options_men = []
    #     self.options_women = []
    #     for key, value in {'men':2,'women':1}.items():
    #         self.driver.get(f'https://www.asos.com/{key}')
    #         for _ in self.driver.find_elements_by_xpath(f'//*[@id="chrome-sticky-header"]/div[2]/div[{value}]/nav/div/div/button[*]/span/span'): 
    #             if _.text not in ['Sale','Gifts','Brands','Outlet','Marketplace']:
    #                 if key == 'men':
    #                     self.options_men.append(_.text)
    #                 else:
    #                     self.options_women.append(_.text)
    #     return self.options_men, self.options_women
    # def products_number(self):
    #      self.total_number_of_products = int(self.driver.find_element_by_xpath('//*[@id="plp"]/div/div/div[2]/div/div[2]/p').text.split()[-2].replace(",",""))
    #      return self.total_number_of_products

    def href_iterate(self):
        self._get_gender_hrefs()
        for self.href in self.all_categories_hrefs:
            for self.page in itertools.count(1,1): #def iterate()
                self.driver.get(f'{self.href}&page={self.page}')
                # print(f'{self.href}&page={self.page}')
                self._extract_links(f'//*[@id="plp"]/div/div/div[2]/div/div[1]/section/article')
                self.go_to_products(self.page)             
                if self.config.scrape_all_website() is True:
                    if self.is_last_page() is True:
                        break
                else:
                    if self.page == self.load_more:
                        break
    
                   
    def is_last_page(self):
            value = self.driver.find_element_by_xpath('//*[@id="plp"]/div/div/div[2]/div/div[2]/progress').get_attribute('value')
            max_value = self.driver.find_element_by_xpath('//*[@id="plp"]/div/div/div[2]/div/div[2]/progress').get_attribute('max')
            if value == max_value:
                return True
            else:
                return False

    def _get_gender_hrefs(self):
        for key,value in self.config.gender_dict.items():
            self.driver.get(self.root + f'{key}')
            self._scrape_category(f'//*[@id="chrome-sticky-header"]/div[2]/div[{value[0]}]/nav/div/div/button[*]', value[1])
            self.all_categories_hrefs.extend(self.gender_hrefs)
        return self.all_categories_hrefs
    
    def _extract_links(self, xpath: str):
        xpaths_list = self.driver.find_elements_by_xpath(xpath)
        self.links = []
        for item in xpaths_list:
            self.links.append(item.find_element_by_xpath(
                './/a').get_attribute('href'))
        #  print(len(self.links))
        return self.links
        #  print(self.links)
     
    def click_buttons(self, button_xpath): 
            try:
                self.driver.find_element_by_xpath(button_xpath).click()
                return True
            except: 
               pass
    
    def _scrape_category(self, xpath:str, category_list: list ):
        self.gender_hrefs = [] #href links to be scraped
        self.category_list = category_list
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
        # print(self.gender_hrefs)   
        return self.gender_hrefs
 
     # this method will extract the products' hrefs products from (page_number = 4) pages
    

    def go_to_products(self, page: int): #rename get_product
        #  n = int(self.config.products_per_category) 
         self.product_dict_list = {}
         self.sub_category_name = self.driver.find_element_by_xpath(
             '//*[@id="category-banner-wrapper"]/div/h1').text.lower().replace(" ", "-").replace(":","").replace("'","")
        
        #  for nr, url in tqdm(itertools.islice(enumerate(self.links,1),n)): 
         for nr, url in tqdm(enumerate(self.links,1)): 
            # self.product_number = nr
            self.product_number = ((page-1)*72) + nr 
            self.driver.get(url)
            self.product_information_dict = {f'{self.sub_category_name}-product-{self.product_number}': 
                                              {'Product Name': [],
                                               'Price': [],
                                               'Product Code': [],
                                               'Colour': [],
                                               'Product Details' : []
                                               }
                                             } 
                                              
            self._get_details() #get_product_details
            self.download_images(self.sub_category_name)
            self.product_dict_list.update(self.product_information_dict)
         self.save_to_json(self.product_dict_list, self.sub_category_name)
         
    def _get_details(self):
        try: #find details info
            for key in self.xpath_dict:
                if key == 'Product Details':
                    details_container = self.driver.find_elements_by_xpath(self.xpath_dict[key])
                    for detail in details_container:
                        self.product_information_dict[f'{self.sub_category_name}-product-{self.product_number}'][key].append(detail.text)

                else:
                    dict_key = self.driver.find_element_by_xpath(self.xpath_dict[key])
                    self.product_information_dict[f'{self.sub_category_name}-product-{self.product_number}'][key].append(dict_key.text)
                        
        except:
            self.product_information_dict[f'{self.sub_category_name}-product-{self.product_number}'][key].append('No information found')
        
        return self.product_information_dict

    def _get_images_src(self):
        self.xpath_src_list = self.driver.find_elements_by_xpath('//*[@id="product-gallery"]/div[1]/div[2]/div[*]/img')
        self.src_list = []                                        
        for xpath_src in self.xpath_src_list:
           self.src_list.append(xpath_src.get_attribute('src'))
    
    def _download_images_locally(self, sub_category_name: str):
         if not os.path.exists(f'images/{sub_category_name}'):
             os.makedirs(f'images/{sub_category_name}')
         
         self._get_images_src()
         for i,src in enumerate(self.src_list[:-1],1):
            urllib.request.urlretrieve(src, f'images/{sub_category_name}/{sub_category_name}-product{self.product_number}.{i}.jpg')
     
    def _save_to_json_locally(self, product_dict_list: dict, sub_category_name:str):
         if not os.path.exists(f'json_files'):
             os.makedirs(f'json_files')
         
         with open(f'json_files/{sub_category_name}_details.json', mode='a+', encoding='utf-8-sig') as f:
            json.dump(product_dict_list, f, indent=4, ensure_ascii=False) 
            f.write('\n')  
            f.close() 

    def _download_images_to_s3(self, sub_category_name: str):
        self._get_images_src()
        with tempfile.TemporaryDirectory() as temp_dir:
            for i,src in enumerate(self.src_list[:-1],1):
                urllib.request.urlretrieve(src, f'{temp_dir}/image_{i}.jpg')
                self.s3_client.upload_file(f'{temp_dir}/image_{i}.jpg','asosscraperbucket',
                                         f'images/{sub_category_name}/{sub_category_name}-product{self.product_number}.{i}.jpg')
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        
    def _save_to_json_to_s3(self, product_dict_list: dict, sub_category_name:str,):
        with tempfile.TemporaryDirectory() as temp_dir:
            with open(f'{temp_dir}/{sub_category_name}_details.json', mode='a+', encoding='utf-8-sig') as f:
                json.dump(product_dict_list, f, indent=4, ensure_ascii=False) #'indent = x' to format output in json file, visually better
                f.write('\n')
                f.flush()
                time.sleep(3)
                self.s3_client.upload_file(f'{temp_dir}/{sub_category_name}_details.json', 'asosscraperbucket', f'json_files/{sub_category_name}_details.json')
                
        if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir) 
    
    def download_images(self, *args):
        if self.config.location == 'local_machine & s3_bucket':
            self.set_s3_connection()
            self._download_images_locally(*args)
            self._download_images_to_s3(*args)

        elif self.config.location == 'local_machine':
            self._download_images_locally(*args)

        elif self.config.location == 's3_bucket':
            self.set_s3_connection()
            self._download_images_to_s3(*args)
                
    def save_to_json(self,*args):
        if self.config.location == 'local_machine & s3_bucket':
            self.set_s3_connection()
            self._save_to_json_locally(*args)
            self._save_to_json_to_s3(*args)

        elif self.config.location == 'local_machine':
            self._save_to_json_locally(*args)
                
        elif self.config.location == 's3_bucket':
            self.set_s3_connection()
            self._save_to_json_to_s3(*args)

    def set_s3_connection(self):
            self.s3_client = boto3.client('s3')
            
if __name__ == '__main__':
    # instance_choices = User_input()
    # instance_choices.scrape_or_not()
    product_search = AsosScraper() 
    product_search.click_buttons(product_search.accept_cookies) #this xpath is for accepting the cookies                         
    product_search.scrape_user_choices()
    product_search.driver.quit()
    


    


