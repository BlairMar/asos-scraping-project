import os
import time
import json
import itertools
import urllib.request
import selenium
import boto3
import tempfile
import shutil
import yaml
import argparse
import pandas as pd
import psycopg2
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from sqlalchemy import create_engine
from tqdm import tqdm

class AsosScraper:
    xpath_dict = {
                'Product Name': '//*[@id="aside-content"]/div[1]/h1',
                'Price': '//*[@id="product-price"]/div/span[2]/span[4]/span[1]',
                'Product Details' : '//*[@id="product-details-container"]/div[1]/div/ul/li',
                'Product Code': '//*[@id="product-details-container"]/div[2]/div[1]/p',                                   
                'Colour': '//*[@id="product-colour"]/section/div/div/span'    
                } 
     
    def __init__(self):
        """
        Class constructor to initialize class variables.
       
        Variables:
            self.root: URL root of website to be scraped
            self.driver: selenium webdriver
            self.config: dictionary object parsed from config.yaml
            self.links: list variable to be used each time extract_links is called
            self.args: CLI arguments 
            self.options_men: list object from config dictionary containing men's subcategories to be scraped
            self.options_women: list object from config dictionary containing women's subcategories to be scraped
            
        """
        with open("config.yaml", 'r') as f:
            self.config = yaml.safe_load(f)

        self.root = "https://www.asos.com/"
        self.links = [] 
        
        # use argparsers to set CLI flags 
        parser = argparse.ArgumentParser(description='Scraper Config')
        parser.add_argument('--CHW', action=argparse.BooleanOptionalAction, default=False) # --CHW to run Chrome
        parser.add_argument('--CH', action=argparse.BooleanOptionalAction, default=True) # --no-CH not to run headless Chrome
        parser.add_argument('--R', action=argparse.BooleanOptionalAction, default=False) # --R for driver.Remote()
        parser.add_argument('--M', action=argparse.BooleanOptionalAction, default=False) # --M for men
        parser.add_argument('--W', action=argparse.BooleanOptionalAction, default=False) # --W for women
        parser.add_argument('--L', action=argparse.BooleanOptionalAction, default=True) # --no-L not to save locally 
        parser.add_argument('--S3', action=argparse.BooleanOptionalAction, default=False) # --S3 to save to S3 bucket
        parser.add_argument('--SJ', action=argparse.BooleanOptionalAction, default=True) # --no-SJ no to save JSON file
        parser.add_argument('--SI', action=argparse.BooleanOptionalAction, default=False) #  --SI to save image 
        parser.add_argument('--DB', action=argparse.BooleanOptionalAction, default=False) # --DB save data into a databse 
        parser.add_argument("-BN", "--BUCKET_NAME", help="Name of your S3 Bucket") #-BN <bucket name> for bucket name
        parser.add_argument("-NUM", "--PRODUCTS_PER_CATEGORY", help="Number of products per category", default='all')  # -NUM to customize number of products
        parser.add_argument("-OM", "--OPTIONS_MEN", help="(1)New in, (2)Clothing, (3)Shoes, (4)Accessories, (5)Topman, (6)Sportswear, (7)Face + Body", default=[0]) # -OM to customize men catgegories
        parser.add_argument("-OW", "--OPTIONS_WOMEN", help="(1)New in, (2)Clothing, (3)Shoes, (4)Accessories, (5)Topshop, (6)Sportswear, (7)Face + Body", default=[0]) # -OW to customize women categories
        parser.add_argument('-N','--DBNAME',help='Type your databse name',default=False) #-N <database name>
        parser.add_argument('-PT','--PORT',help='Type the connection port',default=False) #-PT <connection port>
        parser.add_argument('-PS','--PASSWORD',help='Type your database connection password') #-PS <password>
        self.args = parser.parse_args()
        print(self.args)

        chrome_options = Options()
        #conditions to choose the driver
        # if no user input, the default settings would run Chrome driver
        if self.args.CH == True and self.args.R == False:
            # if self.config['DRIVER'] == 'Chrome':
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--allow-running-insecure-content')        
            chrome_options.add_argument('--no-sandbox')        
            chrome_options.add_argument('--headless')        
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'") 
            chrome_options.add_argument("window-size=1920,1080")
            self.driver = webdriver.Chrome(options=chrome_options)
        
        if self.args.CHW == True:
            self.driver = webdriver.Chrome()
        # if user chooses Remote, then driver = Remote
        if self.args.CH == False and self.args.R == True: # --no-CH
            self.driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME)

        # if by mistake user chooses both Chrome and Remote, run Remote 
        if self.args.CH == True and self.args.R == True: # --no-CH
            print('Your choice is both Chrome and Remote. The driver will run remotely')
            self.driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME)

        self.driver.get(self.root)
        
        # conditions to set the gender
        # by default, both self.config['WOMEN'] & self.config['MEN'] are True, so the scraper would scrape both genders
        # the user can customize the gender and this would override the default configuration
        if self.args.M == True and self.args.W == False:
            self.config['WOMEN'] = False
        elif self.args.M == True and self.args.W == True:
            self.config['MEN'] = True
            self.config['WOMEN'] = True 
        elif self.args.M == False and self.args.W == True:
            self.config['MEN'] = False
        #if no user input, then run default values MEN = True; WOMEN = True
        elif self.args.M == False and self.args.W == False:
            self.config['MEN'] = True
            self.config['WOMEN'] = True 

        # set category options 
        # create a list input_om based on the user choices. If user chooses 1234, input_om becomes ['1','2','3','4']
        input_om = list(set(self.args.OPTIONS_MEN))
        # every integer inside input_om corresponds to a category, as explained in the README
        for _ in range(len(input_om)):
            if input_om[_] == '1':
                input_om[_] = 'New in'
            elif input_om[_] == '2':
                input_om[_] = 'Clothing'
            elif input_om[_] == '3':
                input_om[_] = 'Shoes'
            elif input_om[_] == '4':
                input_om[_] = 'Accessories'
            elif input_om[_] == '5':
                input_om[_] = 'Topman'
            elif input_om[_] == '6':
                input_om[_] = 'Sportswear'
            elif input_om[_] == '7':
                input_om[_] = 'Face + Body'
            else:
                pass
        # same for women
        input_ow = list(set(self.args.OPTIONS_WOMEN))
        for _ in range(len(input_ow)):
            if input_ow[_] == '1':
                input_ow[_] = 'New in'
            elif input_ow[_] == '2':
                input_ow[_] = 'Clothing'
            elif input_ow[_] == '3':
                input_ow[_] = 'Shoes'
            elif input_ow[_] == '4':
                input_ow[_] = 'Accessories'
            elif input_ow[_] == '5':
                input_ow[_] = 'Topshop'
            elif input_ow[_] == '6':
                input_ow[_] = 'Sportswear'
            elif input_ow[_] == '7':
                input_ow[_] = 'Face + Body'
            else:
                pass
       
        # default=False # contains category list if flag used
         
        # by default, self.options_men contains all men categories, as in the default configuration file
        self.options_men = self.config['OPTIONS_MEN']
        # if the user chooses to scrape men categories, then the input_om list is created and replace the default value of self.options_men
        if self.args.OPTIONS_MEN != [0]:
            self.options_men = input_om

        self.options_women = self.config['OPTIONS_WOMEN'] 
        if self.args.OPTIONS_WOMEN != [0]:
            self.options_women = input_ow
        
        # if the user chooses to save to the S3 bucket and inputs a bucket name, then the default configrations would become True 
        if self.args.S3 == True:
            self.bucket_name = self.args.BUCKET_NAME
        
        self.driver.get_screenshot_as_file('ss.png')
            
    def accept_cookies(self): 
        """ 
        Method using selenium to click on accept_cookies webelement/button.
        Returns: 
            True (bool): if the click() method is successfully performed
        """
        try:
            self.driver.find_element(By.XPATH,"//button[@data-testid ='close-button']").click()
            return True
        except: 
            pass

    def _get_all_subcategory_hrefs(self):
        """
        Method to iterate through configured gender(s) and categories to get subcategory hrefs.
        Calls _scrape_category method to determine which subcategory to get.
        Variable: 
            self._all_subcategory_hrefs: initialize list to store subcategory hrefs
        Return:
            self._all_subcategory_hrefs (list): list containing all subcategory hrefs for the choosen gender(s)
        """
        
        self._all_subcategory_hrefs = []
        for key,value in {'MEN':[2, self.options_men], 'WOMEN':[1, self.options_women]}.items():
            if self.config[key] == True:
                self.driver.get(self.root + key)
                self._scrape_category(f'//*[@id="chrome-sticky-header"]/div[2]/div[{value[0]}]/nav/div/div/button[*]', value[1])
                self._all_subcategory_hrefs.extend(self.subcategory_hrefs)
        return self._all_subcategory_hrefs

    def scrape_and_save(self):
        """
        Method to run scraping functionality.
        Iterates through all subcategory hrefs; for every href iterates through required number of pages and scrapes data.
        Calls _get_all_subcategory_hrefs() to get list containing all subcategory hrefs.
        Calls _extract_links() to get each product's href and collect them inside a list. 
        Calls get_product_information() to get details and images from every product.
        Calls save_json_to_location() to store each product details inside a json file that would be stored to configured location. 
        """
        self._get_all_subcategory_hrefs()
        for href in self._all_subcategory_hrefs:
            self.all_products_dictionary = {}
            for page in itertools.count(1,1): #def iterate()
                self.driver.get(f'{href}&page={page}')
                self.sub_category_name = self.driver.find_element(By.XPATH,'//*[@id="category-banner-wrapper"]/div/h1').text.lower().replace(" ", "-").replace(":","").replace("'","")
                self._extract_links(f'//*[@id="plp"]/div/div/div[2]/div/div[1]/section/article/a', 'href')
                time.sleep(1)          
                self._get_product_information(page)
                if self.args.PRODUCTS_PER_CATEGORY == 'all':
                    if self._is_last_page():
                        break
                else:
                    self.load_more = int(self.args.PRODUCTS_PER_CATEGORY) // 72
                    if page == self.load_more + 1:
                        break
            if self.args.DB == True:        
                self._create_dataframe(self.all_products_dictionary,self.sub_category_name)
            if  self.args.SJ == True: #user needs --no-SJ to stop this action
                self._save_json(self.all_products_dictionary, self.sub_category_name)
       
    def _is_last_page(self):
        """
        Method to get the maximum number of products from subcategory. 
        
        Returns:
            True (bool): If the number of products viewed is equal to the maximum number of products. 
            False (bool): If the number of products viewed is not equal to the maximum number of products. 
        """
        value = self.driver.find_element(By.XPATH,'//*[@id="plp"]/div/div/div[2]/div/div[2]/progress').get_attribute('value')
        max_value = self.driver.find_element(By.XPATH,'//*[@id="plp"]/div/div/div[2]/div/div[2]/progress').get_attribute('max')
        if value == max_value:
            return True
        else:
            return False

    def _extract_links(self, xpath: str, attribute = 'href' or 'src'):
        """
        Method to extract either the href or src attributes from webelements. 
        Parameters:
            xpath (str): xpath of webelement containing one of the attributes: 'href' or 'src'
            attribute (str): webelement attribute that can be either 'href' or 'src' 
        Returns:
            self.links (list): list stores the extracted 'href's or 'src's
        """
        xpaths_list = self.driver.find_elements(By.XPATH,(xpath))
        self.links = []
        for item in xpaths_list:
            self.links.append(item.get_attribute(attribute))
        return self.links
         
    def _scrape_category(self, xpath:str, category_list: list ):
        """
        Method to return href's of webpages to be scraped, according to the user's choices.
        For every main gender category, the method extracts the 'View all' or 'New in' subcategory hrefs.
        
        Parameters: 
            xpath (str): requires a string type input for either the 'Men' and/or 'Women' sections.
            category_list (list): requires a list type input containing the category opetions determined in the config.yaml.
            
        Return:
            self.subcategory_hrefs (list): list containing subcategory_hrefs for given gender.
            This would be appended to self.all_subcategory_hrefs inside _get_all_subcategory_hrefs method.
        """
        
        self.subcategory_hrefs = [] #href links to be scraped
        self.category_list = category_list
        category_list_to_dict = []  
        main_category_elements = self.driver.find_elements(By.XPATH,(xpath))
       
        #create a list category_list_to_dict that contains the category name, the index number of the category button and the corresponding webelement
        for element in main_category_elements:
            main_category_heading = element.find_element(By.CSS_SELECTOR,'span span').text
            if main_category_heading in self.category_list:  
                category_list_to_dict.append(main_category_heading) 
                category_list_to_dict.append(int(element.get_attribute('data-index')) + 1) 
                category_list_to_dict.append(element) 
        
        #transform categroy_list_to_dict into a dictionary containing the category names as a keys, and index_number and webelement as values
        category_dict = {category_list_to_dict[i]:[category_list_to_dict[i + 1],category_list_to_dict[i + 2]] for i in range(0, len(category_list_to_dict), 3)}  
        
        #for every category, in category_dict, get the href for either 'View all' or 'New in' subcatgories. If both 'View all' and 'New in' exist within category, get 'View all' href 
        subcategory_elements_list = [] 
        for i, (key, elements) in enumerate(category_dict.items()): 
            elements[1].click()  
            time.sleep(3)

            subcategory_elements_list.append(self.driver.find_elements(By.XPATH, f'//div[{elements[0]}]/div/div[2]/ul/li[1]/ul/li/a'))          
            for element in subcategory_elements_list[i]:  
                if element.text == 'View all':
                    self.subcategory_hrefs.append(element.get_attribute('href'))
                    break
                elif element.text == 'New in': 
                    temp = element        
            else:
                self.subcategory_hrefs.append(temp.get_attribute('href'))     
        return self.subcategory_hrefs 
 
    def _get_number_of_products(self):
        """
        Method to set how many products (n) will be scraped. 
        If the value of the configured number of products is 'all', all the products will be scraped.
        If the value of the configured number of products is an integer, the number of products to be scraped is determined by the integer.
            
        Returns:
            n (int): number of products to be scraped.
        """
        if self.args.PRODUCTS_PER_CATEGORY == 'all':
            n = int(self.driver.find_element(By.XPATH, '//*[@id="plp"]/div/div/div[2]/div/div[2]/progress').get_attribute('max'))
            return n
        else:
            n = int(self.args.PRODUCTS_PER_CATEGORY)
            return n
    
    def _get_product_information (self, page: int): 
        """
        Method to go to every product on page and get product information: images & product details.
        This method calls two other instance methods: _get_details() and save_image_to_location()
        Parameters: 
            page (int): the page number of the website subcategory 
            This parameter is determined within the 'scrape_and_save' method.
        Returns: 
            self.all_products_dictionary (dict): a dictionary containing individual product details dictionaries (product_information_dict).
        """
        # iterate through the list with products href until the product number equals the number of products set by the user 
        n = self._get_number_of_products()
        for nr, url in tqdm(itertools.islice(enumerate(self.links,1),n)): 
            self.product_number = ((page-1)*72) + nr 
            self.driver.get(url)                               
            #for every product, get details and dowloand images (if requested by the user). Details are stored as nested dictionary within all_products_dictionary
            self.driver.get_screenshot_as_file('ss1.png')
            self._get_details()
            if self.args.SI == True: 
                self._save_image(self.sub_category_name)
            self.all_products_dictionary.update(self.product_information_dict)
            # if the product number reaches the limit imposed by the user, stop iterating through the list with products hrefs
            if self.product_number == n:
                break
        
        # all_products_dictionary is converted to json format when save_json method is called inside scrape_and_save method
        return self.all_products_dictionary
        
    def _get_details(self):
        """
        Method to get product information and details and store them into a dictionary.
        Variables:
            unique_product_name: unique product identifier determined by the gender, subcategory name and order on the webpage
            product_information_dict: dictionary template to which the product details are extracted. 
            xpath_dict: xpath lookup to access the details to be scraped on each product page 
        Return: 
            self.product_information_dict (dict): dictionary storing product information and details
                Every product_information_dict is added to the all_products_dictionary inside get_product_information method
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
            try: 
                # ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)
                if key == 'Product Details':
                    # details_container =  WebDriverWait(self.driver, 5, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located(By.XPATH, (self.xpath_dict[key])))
                    self.driver.find_element(By.XPATH,'//*[@id="product-details-container"]/div[4]/div/a[1]').click()
                    details_container = self.driver.find_elements(By.XPATH, (self.xpath_dict[key]))
                    for detail in details_container:
                        time.sleep(0.5)
                        self.product_information_dict[unique_product_name][key].append(detail.text)
                
                if key == 'Colour':
                    dict_key = self.driver.find_element(By.XPATH,(self.xpath_dict[key]))
                    if dict_key.text == '':
                        color_options = self.driver.find_element(By.XPATH, '//*[@id="product-colour"]/section/div/div/div/select')
                        select = Select(color_options)
                        options_list = select.options
                        for option in options_list[1:]:
                            self.product_information_dict[unique_product_name][key].append(option.text)  
                    else:
                        self.product_information_dict[unique_product_name][key].append(dict_key.text)
                        
                else:
                    # dict_key = WebDriverWait(self.driver, 5, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located(By.XPATH,(self.xpath_dict[key])))
                    dict_key = self.driver.find_element(By.XPATH,(self.xpath_dict[key]))
                    self.product_information_dict[unique_product_name][key].append(dict_key.text)
                     
            except:
                self.product_information_dict[unique_product_name][key].append('No information found')
        
        return self.product_information_dict

    def _save_image(self, sub_category_name: str):
        """
        Method to download every product image (jpg format) to local and/or s3_bucket locations.
    
        Parameters: 
            sub_category_name (str): parameter determined within the get_product_information method.
        """
        image_category = sub_category_name
        image_name = f'{sub_category_name}-product{self.product_number}'
        src_list = self._extract_links('//*[@id="product-gallery"]/div[2]/div[2]/div[*]/img','src')
        # //*[@id="product-gallery"]/div[2]/div[2]/div[2]/img
        
        if self.args.L == True:
            image_path = f'images/{image_category}'
            if not os.path.exists(image_path):
                os.makedirs(image_path)         
            for i,src in enumerate(src_list[:-1],1):   
                urllib.request.urlretrieve(src, f'{image_path}/{image_name}.{i}.jpg')   
           
        if self.args.S3 == True:
            self.set_s3_connection()
            with tempfile.TemporaryDirectory() as temp_dir:
                for i,src in enumerate(src_list[:-1],1):   
                    urllib.request.urlretrieve(src, f'{temp_dir}/{image_name}.{i}.jpg')
                    self.s3_client.upload_file(f'{temp_dir}/{image_name}.{i}.jpg', self.bucket_name, f'images/{image_category}/{image_name}.{i}.jpg')
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            
    def _save_json(self, all_products_dictionary, sub_category_name):
        """
        Method to convert the all_products_dictionary object into a json format and download it into local and/or s3_bucket locations.
        Parameters: 
            sub_category_name (str): parameter determined within the get_product_information method. 
            all_products_dictionary (dict): dictionary to be converted into json file; this parameter is determined within the get_product_information_ method.
        """
        file_to_convert = all_products_dictionary
        file_name = f'{sub_category_name}-details.json'

        if self.args.L == True:
            if not os.path.exists('json-files'):
                os.makedirs('json-files')
            with open(f'json-files/{file_name}', mode='a+', encoding='utf-8-sig') as f:
                json.dump(file_to_convert, f, indent=4, ensure_ascii=False) 
                f.write('\n') 
        
        if self.args.S3 == True:
            self.set_s3_connection()
            with tempfile.TemporaryDirectory() as temp_dir:
                with open(f'{temp_dir}/{file_name}', mode='a+', encoding='utf-8-sig') as f:
                    json.dump(file_to_convert, f, indent=4, ensure_ascii=False) 
                    f.write('\n') 
                    f.flush()
                    time.sleep(3)
                    self.s3_client.upload_file(f'{temp_dir}/{file_name}', self.bucket_name, f'json_files/{file_name}')
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

    def set_s3_connection(self):
        """
        Method to create service client connection to the S3 AWS services.
        Returns:
            self.s3_client: variable name for the s3 client connection 
        """
        self.s3_client = boto3.client('s3')
        return self.s3_client


    def _create_dataframe(self, all_products_dictionary,sub_category_name):
        """
        Method to create pandas dataframe to manipulate json data format. 
        """
        # import collected data to pandas dataframe
        df = pd.DataFrame(all_products_dictionary)
        df_t = df.transpose()
        # clean data so that it is not displayed in lists but in strings and strip unwanted characters 
        for row in range(len(df_t)):
            df_t['Product Name'][row] = self._listToString(df_t['Product Name'][row])
            df_t['Price'][row] = self._listToString(df_t['Price'][row]).strip('Â Now')
            df_t['Product Code'][row] = self._listToString(df_t['Product Code'][row])
        df_t = df_t.reset_index()
        df_t.rename({'index':'Categroy & product number'}, axis=1, inplace=True)
        # connect to PostgreSQL database
        self._connect_to_RDS()
        # save data to SQL in tables named by the scraped subcategory
        df_t.to_sql(f'ASOS_{sub_category_name}', self.engine, if_exists = 'replace')

    def _listToString(self,string): 
        """
        Method to transform list into string.
        
        Returns:
            created_string (str)
        """
        # initialize an empty string
        created_string = "" 
        # traverse in the string  
        for ele in string: 
            created_string += ele  
        # return string  
        return created_string 

    def _connect_to_RDS(self):
        """
        Method to connect to PostgreSQL database using psycopg2. 
        Variables: 
            DATABASE_TYPE (str): 'ostgreSQL' by default
            DBAPI (str): 'psycopg2' by default
            USER (str): 'postgres' by default
            PASSWORD (str): needs user input 
            PORT (str): uses user input or 5432 as default
            DATABASE (str): uses user input or 'Pagila' as default
            HOST (str): 'localhost' by default 
        
        Returns:
            self.engin: the engine to connect to the PostgreSQL database.
        """
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        USER = 'postgres'
        # User's for a conenction password.
        PASSWORD = str(self.args.PASSWORD)
        # User's connection port, if none given, default to 5432.
        if self.args.PORT == True:
            PORT = int(self.args.PORT)
        else:
            PORT = 5432
        # User's database name, if none given, default to Pagila.
        if self.args.DBNAME == True:
            DATABASE = str(self.args.DBNAME)
        else:
            DATABASE = 'Pagila'
        HOST = 'localhost'
        # Create engine to connect to databse using both default and user inputs 
        self.engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
        # Connect to the RDS
        self.engine.connect()
        return self.engine

if __name__ == '__main__':
    product_search = AsosScraper()
    product_search.accept_cookies()                     
    product_search.scrape_and_save()
    product_search.driver.quit()
