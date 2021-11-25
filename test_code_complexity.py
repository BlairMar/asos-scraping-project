import time

from selenium.webdriver.remote.webdriver import WebDriver
from input_file import User_input
import selenium
from selenium import webdriver



# driver = webdriver.Chrome()

start_time = time.time()
list_all_products = []
for xpath in range(72):
    list_all_products.append(xpath)
# print(len(list_all_products))

def go_to_product():
    for product in list_all_products:
        get_details()
        download_images()

def get_details():
    for j in range(5):
        if j == 5:
            for j1 in range(8):
                return j1
        else:
            return j
    
def download_images():
    for src in range(4):
        return src

def test_complexity_1():
    for _ in range(31):
        go_to_product()
    print(time.time()-start_time)

# test_complexity_1()

def test_complexity_2():
    list_all_products1 = []
    for _ in range(31):
        for xpath in range(72):
            list_all_products1.append(xpath)
    go_to_product()
    print(time.time()-start_time)

test_complexity_2()
# instance_choices = User_input()
# instance_choices.scrape_or_not()
# if instance_choices.scrape_all_website():
#     print('function is running')
# else:
#     print('function is not running')
    
# driver.get('https://www.asos.com/women/new-in/new-in-accessories/cat/?cid=27109&nlid=ww|accessories|shop+by+product|new+in')
# # time.sleep(2)
# # button1 = driver.find_element_by_xpath("//button[@data-testid ='close-button']")
# # # button1 = driver.find_element_by_id("close-button")

# # print(button1)
# # button1.click()
# # button = driver.find_element_by_xpath("//a[@data-auto-id ='loadMoreProducts']")
# # print(button)
# # button.click()
# # "//button[@data-testid ='close-button']"
# def load_more_Scrape_all(xpath):
#          if instance_choices.scrape_all_website():
#             try:
#                 while True:
#                     button1 = driver.find_element_by_xpath(xpath)
#                     button1.click()
#                     time.sleep(1)
#                     print('Load more has been clicked')
#             except:
#                 print('done!')
#                 pass
#          print('uiii')
        
# load_more_Scrape_all("//button[@data-testid ='close-button']")
# load_more_Scrape_all("//a[@data-auto-id ='loadMoreProducts']")

# #%%
# user_input = 0
# breakpoint = user_input // 72
# def function():  

#     while True:
#         user_input = user_input + 1
#         yield user_input  
#         if user_input == breakpoint:
#             break 

# for count, user_input in enumerate(function()):
#     print(count, user_input)
        


    
# # %%
# def click_button():
#         counter = 0
#         break_point = 3
#         while True:
#             counter = counter + 1
#             try:
#                 print('hey')
#             except:
#                 break
#             time.sleep(1)
#             yield counter
#             if break_point == counter:
#                break
#         print(counter)  
# click_button()


# %%
uiii = []
name = ['Miruna', 'James']
for n in name:
    for _ in range(1,2):
        name1 = f"{n}&page={_}"
        uiii.append(name1)
print(uiii)


# %%
for i in range(1, i + 1):
    while (i + 1 < 5):
        print(i)
# %%
# button = driver.find_element_by_xpath("//a[@data-auto-id ='loadMoreProducts']")

def _load_more_products(self): 
         for _ in range(self.load_more + 1):
             self.click_buttons("//a[@data-auto-id ='loadMoreProducts']")

         sections_xpaths_list = []
         for _ in range(1, self.load_more + 2): #load_more + 2 = page_number
            sections_xpaths_list.append(f'//*[@id="plp"]/div/div/div[2]/div/div[1]/section[{_}]/article')  
         
         list_all_products = []
         for section_xpath in sections_xpaths_list:# for every section(page with 72 products) use the "extract_links" method to extract the hrefs for every product on the page
             self._extract_links(section_xpath)
             list_all_products += self.links  #self.links will extract 72 hrefs for every section_xpath and will be added to the list_all_products
         self.product_urls = list_all_products # save the list with hrefs in another variable that will be reffered to in the following methods
         time.sleep(2)
     
def click_buttons(self, button_xpath): 
            try:
                self.driver.find_element_by_xpath(button_xpath).click()
                return True
            except: 
               pass
def scrape_user_choices(self):
    self._get_gender_hrefs()
    for href in self.all_categories_hrefs:
        self.product_urls = []
        for page in range(1, self.load_more + 2):
            self.driver.get(f'{href}&page={page}')
            print(f'{href}&page={page}')
            self.product_urls_per_page = self._extract_links(f'//*[@id="plp"]/div/div/div[2]/div/div[1]/section/article')
            self.product_urls.extend(self.product_urls_per_page)
        # print(len(self.product_urls))
        self.go_to_products()


#%%
import selenium
from selenium import webdriver
import itertools


class New:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.href = 'https://www.asos.com/men/new-in/new-in-shoes/cat/?cid=17184&nlid=mw|shoes|shop+by+product|new+in'

    def method1(self):
        for page in itertools.count(1,1): #def iterate()
                self.driver.get(f'{self.href}&page={page}')
                print(f'{self.href}&page={page}')
                self.product_urls_per_page = self._extract_links(f'//*[@id="plp"]/div/div/div[2]/div/div[1]/section/article')
                if scrape_all_website() is True:
                    self.iterate()
                    if self.is_last_page() is True:
                        break
                else:
                    if page == self.load_more
                    self.iterate()
                    self.is_last_page
                   


    
    def is_last_page(self):
            value = self.driver.find_element_by_xpath('//*[@id="plp"]/div/div/div[2]/div/div[2]/progress').get_attribute('value')
            max_value = self.driver.find_element_by_xpath('//*[@id="plp"]/div/div/div[2]/div/div[2]/progress').get_attribute('max')
            if value == max_value:
                return True
            else:
                return False
class_instance = New()
class_instance.method1()





# %%
    def is_last_page(self):
            value = driver.find_element_by_xpath('//*[@id="plp"]/div/div/div[2]/div/div[2]/progress').get_attribute('value')
            max_value = driver.find_element_by_xpath('//*[@id="plp"]/div/div/div[2]/div/div[2]/progress').get_attribute('max')
            if value == max_value:
                return True
            else:
                return False

#%%
 


#%%
import selenium
from selenium import webdriver
import itertools

driver = webdriver.Chrome()
def get_options_lists(self):
    options_men = []
    options_women = []
    for key, value in {'men':2,'women':1}.items():
        driver.get(f'https://www.asos.com/{key}')
        for _ in driver.find_elements_by_xpath(f'//*[@id="chrome-sticky-header"]/div[2]/div[{value}]/nav/div/div/button[*]/span/span'): 
            if _.text not in ['Sale','Gifts','Brands','Outlet','Marketplace']:
                if key == 'men':
                    options_men.append(_.text)
                else:
                    options_women.append(_.text)
    return options_men, options_women
# %%
