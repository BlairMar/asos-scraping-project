import os
import time
import json
import itertools
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
import yaml


class AsosScraper:
    xpath_dict = {
                'Product Name': '//*[@id="aside-content"]/div[1]/h1',
                'Price': '//*[@id="product-price"]/div/span[2]/span[4]/span[1]',
                'Product Details' : '//*[@id="product-details-container"]/div[1]/div/ul/li',
                'Product Code': '//*[@id="product-details-container"]/div[2]/div[1]/p',                                   
                'Colour': '//*[@id="product-colour"]/section/div/div/span'    
                } 

    accept_cookies = "//button[@data-testid ='close-button']"
    with open("config.yaml", 'r') as f:
        config = yaml.safe_load(f)
     
    def __init__(self):
        """
        Class constructor to initialize class variables.
       
        Variables:
            self.root: URL root of website to be scraped
            self.driver: selenium webdriver
            self.config: dictionary object parsed from config.yaml
            self.options_men: list object from config dictionary containing men's subcategories to be scraped
            self.options_women: list object from config dictionary containing women's subcategories to be scraped
            self.links: list variable to be used each time extract_links is called
        """
        self.root = "https://www.asos.com/"
        if self.config['driver'] == 'Chrome':
            self.driver = webdriver.Chrome()
        else:
            self.driver = webdriver.Remote("http://localhost:4444/wd/hub", DesiredCapabilities.CHROME)
        self.driver.get(self.root)
        self.options_men = self.config['options_men']
        self.options_women = self.config['options_women']
        self.links = []  
    
        # if self.config['s3_bucket'] == True:
        #     self.set_s3_connection()
        #     self.temp_dir = tempfile.TemporaryDirectory()
    def _get_all_subcategory_hrefs(self):
        """
        Method to iterate through configured gender(s) and categories to get subcategory hrefs.
        Calls _scrape_category method to determine which subcategory to get.

        Variable: 
            self._all_subcategory_hrefs: initialize list to store subcategory hrefs

        Return:
            self._all_subcategory_hrefs: list containing all subcategory hrefs
        """
        self._all_subcategory_hrefs = []
        for key,value in {'men':[2, self.options_men], 'women':[1, self.options_women]}.items():
            if self.config[key] == True:
                self.driver.get(self.root + key)
                self._scrape_category(f'//*[@id="chrome-sticky-header"]/div[2]/div[{value[0]}]/nav/div/div/button[*]', value[1])
                self._all_subcategory_hrefs.extend(self.gender_hrefs)
        return self._all_subcategory_hrefs
        
    def href_iterate(self):
        """
        Method to run scraping functionality.
        Iterates through all subcategory hrefs; for every href iterates through required number of pages as 
   
        Variable:
            
        """
        self._get_all_subcategory_hrefs()
        for href in self._all_subcategory_hrefs:
            self.all_products_dictionary = {}
            for page in itertools.count(1,1): #def iterate()
                self.driver.get(f'{href}&page={page}')
                self.sub_category_name = self.driver.find_element_by_xpath('//*[@id="category-banner-wrapper"]/div/h1').text.lower().replace(" ", "-").replace(":","").replace("'","")
                self._extract_links(f'//*[@id="plp"]/div/div/div[2]/div/div[1]/section/article/a', 'href')
                print(page)
                time.sleep(1)          
                self.get_product_information(page)
                if self.config['products_per_category'] == 'all':
                    if self.is_last_page():
                        break
                else:
                    self.load_more = int(self.config['products_per_category']) // 72
                    if page == self.load_more + 1:
                        break
            self.save_json_to_location(self.all_products_dictionary, self.sub_category_name)
       
    def is_last_page(self):
            value = self.driver.find_element_by_xpath('//*[@id="plp"]/div/div/div[2]/div/div[2]/progress').get_attribute('value')
            self.max_value = self.driver.find_element_by_xpath('//*[@id="plp"]/div/div/div[2]/div/div[2]/progress').get_attribute('max')
            if value == self.max_value:
                return True
            else:
                return False
    def get_number_of_products(self):
        if self.config['products_per_category'] == 'all':
            n = self.max_value
            return n 
        else:
            n = int(self.config['products_per_category'])
            return n



    
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
            
            These parameters are determined within the '_get_all_subcategory_hrefs' method.
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

    def get_number_of_products(self):
        if self.config['products_per_category'] == 'all':
            n = self.driver.find_element_by_xpath('//*[@id="plp"]/div/div/div[2]/div/div[2]/progress').get_attribute('max')
            return n
        else:
            n = int(self.config['products_per_category'])
            return n
    

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
        n = self.get_number_of_products()
        for nr, url in tqdm(itertools.islice(enumerate(self.links,1),n)): 
        # for nr, url in tqdm(enumerate(self.links,1)): 
            self.product_number = ((page-1)*72) + nr 
            self.driver.get(url)                               
            self._get_details() #get_product_details
            self.save_image_to_location(self.sub_category_name)
            self.all_products_dictionary.update(self.product_information_dict)
            if self.product_number == n:
                break
        return self.all_products_dictionary
        # self.save_json_to_location(self.all_products_dictionary, self.sub_category_name)
         
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
    def _get_src_and_download_image(self, image_path, image_category, image_name):
        """
        Method to get the src for every product image and download the image to a given location
        Parameteres: 
            filename: location where the images are downloaded to 
        
        Variables: 
            scr_list: list into which the obtained src is stored
        """
       
    #save images to location
    def save_image_to_location(self, sub_category_name):
        image_category = sub_category_name
        image_name = f'{sub_category_name}-product{self.product_number}'
        src_list = self._extract_links('//*[@id="product-gallery"]/div[1]/div[2]/div[*]/img','src')
        
        if self.config['local'] == True:
            image_path = f'images/{image_category}'
            if not os.path.exists(image_path):
                os.makedirs(image_path)         
            for i,src in enumerate(src_list[:-1],1):   
                urllib.request.urlretrieve(src, f'{image_path}/{image_name}.{i}.jpg')   
           
        if self.config['s3_bucket'] == True:
            self.set_s3_connection()
            with tempfile.TemporaryDirectory() as temp_dir:
                for i,src in enumerate(src_list[:-1],1):   
                    urllib.request.urlretrieve(src, f'{temp_dir}/{image_name}.{i}.jpg')
                    self.s3_client.upload_file(f'{temp_dir}/{image_name}.{i}.jpg', 'asosscraperbucket2', f'images/{image_category}/{image_name}.{i}.jpg')
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            
    def save_json_to_location(self, all_products_dictionary, sub_category_name):
        file_to_convert = all_products_dictionary
        file_name = f'{sub_category_name}-details.json'

        if self.config['local'] == True:
            if not os.path.exists('json-files'):
                os.makedirs('json-files')
            with open(f'json-files/{file_name}', mode='a+', encoding='utf-8-sig') as f:
                json.dump(file_to_convert, f, indent=4, ensure_ascii=False) 
                f.write('\n') 
        
        if self.config['s3_bucket'] == True:
            self.set_s3_connection()
            # temp_dir = tempfile.TemporaryDirectory()
            with tempfile.TemporaryDirectory() as temp_dir:
                with open(f'{temp_dir}/{file_name}', mode='a+', encoding='utf-8-sig') as f:
                    json.dump(file_to_convert, f, indent=4, ensure_ascii=False) 
                    f.write('\n') 
                    f.flush()
                    time.sleep(3)
                    self.s3_client.upload_file(f'{temp_dir}/{file_name}','asosscraperbucket2', f'json_files/{file_name}')
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

    def set_s3_connection(self):
        self.s3_client = boto3.client('s3')
          
if __name__ == '__main__':
    # instance_choices = User_input()
    # instance_choices.scrape_or_not()
    product_search = AsosScraper()
    # product_search.read_from_config_file() 
    product_search.click_buttons(product_search.accept_cookies) #this xpath is for accepting the cookies                           
    product_search.href_iterate()
    product_search.driver.quit()
    # product_search.print_statements()


    



