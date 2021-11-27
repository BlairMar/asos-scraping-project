#%%
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
        print(self.config.gender_dict)
        self._get_gender_hrefs()
        for href in self.all_categories_hrefs:
            for page in itertools.count(1,1): #def iterate()
                self.driver.get(f'{href}&page={page}')
                # print(f'{self.href}&page={self.page}')
                self._extract_links(f'//*[@id="plp"]/div/div/div[2]/div/div[1]/section/article/a', 'href')
                print(page)
                time.sleep(1)
                self.get_product_information(page)             
                if self.config.variable1 is True:
                    if self.is_last_page():
                        break
                else:
                    self.load_more = self.config.products_per_category // 72
                    if page == self.load_more:
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
    
    def _extract_links(self, xpath: str, attribute = 'href' or 'src'):
        xpaths_list = self.driver.find_elements_by_xpath(xpath)
        self.links = []
        for item in xpaths_list:
            self.links.append(item.get_attribute(attribute))
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
        """
        Method to return href's of webpages to be scraped, according to the user's choices.
        For every main gender category, the method extracts extracts the 'View all' or 'New in' subcategory hrefs.
        
        Parameters: 
            xpath: requires a string type input for either the 'Men' or 'Women' sections
            category_list: requires a list type input containing the categories choosen by the user
            
            These parameters are determined within the '_get_gender_hrefs' method.

        Return:
            List with the subcategories hrefs.
        """
        
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
    

    def get_product_information (self, page: int): #rename get_product
        """
        Method to go to every product on page and get product information: images & product details.
        # This method calls three other instance methods: _get_details, _download_images, _save_to_json.

        Parameters: 
            page: the page number of the website subcategory 
            This parameter is determined within the 'href_iterate' method.

        Variable:
            self.product_dict_list = a dictionary that is updated with every product's dictionary with details
        """
        
        n = int(self.config.products_per_category) 
        self.all_products_dictionary = {}
        self.sub_category_name = self.driver.find_element_by_xpath(
            '//*[@id="category-banner-wrapper"]/div/h1').text.lower().replace(" ", "-").replace(":","").replace("'","")
        for nr, url in tqdm(itertools.islice(enumerate(self.links,1),n)): 
        # for nr, url in tqdm(enumerate(self.links,1)): 
            self.product_number = ((page-1)*72) + nr 
            self.driver.get(url)                               
            self._get_details() #get_product_details
            self.save_image_to_location1(self.sub_category_name)
            self.all_products_dictionary.update(self.product_information_dict)
        self.save_json_to_location1(self.all_products_dictionary, self.sub_category_name)
         
    def _get_details(self):
        """
        Method to extract the product details into a dictionary.

        Variables:
            unique_product_name: unique product identifier determined by the gender, subcategory name and order on the webpage
            product_information_dict: dictionary template to which the product details are extracted
            xpath_dict: xpath lookup to access the details to be scraped on each product page 

        Return: 
            dictionary with product details
        """
        unique_product_name = f'{self.sub_category_name}-product-{self.product_number}'
        self.product_information_dict = {unique_product_name: 
                                              {'Product Name': [],
                                               'Price': [],
                                               'Product Code': [],
                                               'Colour': [],
                                               'Product Details' : []
                                               }
                                             } 
        for key in self.xpath_dict:
            try: #find details info
                if key == 'Product Details':
                    details_container = self.driver.find_elements_by_xpath(self.xpath_dict[key])
                    for detail in details_container:
                        self.product_information_dict[unique_product_name][key].append(detail.text)
                else:
                    dict_key = self.driver.find_element_by_xpath(self.xpath_dict[key])
                    self.product_information_dict[unique_product_name][key].append(dict_key.text)
                     
            except:
                self.product_information_dict[unique_product_name][key].append('No information found')
        
        return self.product_information_dict

    #get src and download
    def _get_src_and_download_image(self, image_path, image_name):
        """
        Method to get the src for every product image and download the image to a given location

        Parameteres: 
            filename: location where the images are downloaded to 
        
        Variables: 
            scr_list: list into which the obtained src is stored
        """
        self._extract_links('//*[@id="product-gallery"]/div[1]/div[2]/div[*]/img','src')
        for i,src in enumerate(self.links[:-1],1):
            self.image_path_and_name = image_path + image_name + f'.{i}.jpg'
            urllib.request.urlretrieve(src, self.image_path_and_name)
            if 's3_bucket' in self.config.location:
                self.set_s3_connection()
                self.s3_client.upload_file(self.image_path_and_name, 'asosscraperbucket', f'images/{image_name}.{i}.jpg')
                
        
    #save images to location
    # version 1
    def save_image_to_location1(self, sub_category_name):
        image_path = 'images/'+ sub_category_name 
        image_name = f'/{sub_category_name}-product{self.product_number}'
        def save_image_locally():
                if not os.path.exists(image_path):
                    os.makedirs(image_path)                
                self._get_src_and_download_image(image_path, image_name)
        
        def save_image_to_s3bucket():
                with tempfile.TemporaryDirectory() as temp_dir:
                    self._get_src_and_download_image(temp_dir, image_name)
            
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
        
        if 'local_machine' in self.config.location:
            save_image_locally()
        else:
            pass
        
        if 's3_bucket' in self.config.location:
            save_image_to_s3bucket()
        else:
            pass
        
    # version 2
    def save_image_to_location2(self,sub_category_name):
        image_path = 'images/'+ sub_category_name
        image_name = f'{sub_category_name}-product{self.product_number}.{self.product_image_number}.jpg'
        
        if 'local_machine' in self.config.location:
            self._download_images_locally(image_path, image_name)
        else:
            pass
        
        if 's3_bucket' in self.config.location:
            self._download_images_to_s3(image_path, image_name)
        else: 
            pass
        
    def _download_images_locally(self, image_path: str, image_name:str):
        if not os.path.exists(image_path):
                 os.makedirs(image_path)        
        self._get_src_and_download_image(f'{image_path}/{image_name}')
        
    def _download_images_to_s3(self, image_path: str, image_name:str):
        self.set_s3_connection()
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_name = f'{temp_dir}/{image_path}/{image_name}'
            self._get_src_and_download_image(temp_name)
            self.s3_client.upload_file(temp_name,'asosscraperbucket',f'{image_path}/{image_name}')

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    #***************


    def _save_to_json(self, file_to_convert, file_name):
        with open(file_name, mode='a+', encoding='utf-8-sig') as f:
            json.dump(file_to_convert, f, indent=4, ensure_ascii=False) 
            f.write('\n')  
            if self.config.location == 's3_bucket':
                f.flush()
                time.sleep(3)
            else:
                pass

    # save_json_to_location
    # version 1
    def save_json_to_location1(self, all_products_dictionary, sub_category_name):
        file_to_convert = all_products_dictionary
        file_name = f'json-files/{sub_category_name}-details.json'
    
        def save_json_locally():
            if not os.path.exists('json-files'):
                os.makedirs('json-files')
            self._save_to_json(file_to_convert,file_name)

        def save_json_to_s3bucket():
            self.set_s3_connection()
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_file_name = f'{temp_dir}/{file_name}'
                self._save_to_json(file_to_convert ,file_name)
                self.s3_client.upload_file(temp_file_name,'asosscraperbucket',file_name)
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        
        if 'local_machine' in self.config.location:
            save_json_locally()
        else:
            pass
        
        if 's3_bucket' in self.config.location:
            save_json_to_s3bucket
        else:
            pass

    # version 2
    def save_json_to_location2(self, all_products_dictionary, sub_category_name):
        file_to_convert = all_products_dictionary
        file_name = f'json-files/{sub_category_name}-details.json'

        if 'local_machine' in self.config.location:
            self.save_json_locally(file_to_convert, file_name)
        else:
            pass
            
        if 's3_bucket' in self.config.location:
            self.save_json_to_s3bucket(file_to_convert, file_name)
        else:
            pass
        
    def save_json_locally(self, file_to_convert, file_name):
        if not os.path.exists('json-files'):
            os.makedirs('json-files')
        self._save_to_json(file_to_convert,file_name)
    
    def save_json_to_s3bucket(self, file_to_convert ,file_name):
        self.set_s3_connection()
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_name = f'{temp_dir}/{file_name}'
            self._save_to_json(file_to_convert ,file_name)
            self.s3_client.upload_file(temp_file_name,'asosscraperbucket',file_name)
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

    #**************
    def set_s3_connection(self):
        self.s3_client = boto3.client('s3')
          
if __name__ == '__main__':
    # instance_choices = User_input()
    # instance_choices.scrape_or_not()
    product_search = AsosScraper() 
    product_search.click_buttons(product_search.accept_cookies) #this xpath is for accepting the cookies                           
    product_search.href_iterate()
    product_search.driver.quit()
    


    



# %%
