from pprint import pprint
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

class AsosScraper:
    def __init__ (self, driver = webdriver.Chrome(), webpage ="https://www.asos.com/men"):
        self.driver = driver
        self.webpage = webpage
        driver.get(self.webpage)
        self.a = ActionChains(self.driver)   #object of ActionChains; it ads hover over functionality 
        
    # webpage = ROOT (https://www.asos.com/) + 'men'/'women'
    # gender_list =  
    def men_click_buttons(self):     
        '''
        This function performs hover over and click functions 

        Attributes: 
            category_button : the driver will find this element by xpath 
            sub_categeory_button_clothing_new_in =  the driver finds an element from the submenu obtained by hovering over the category_button
            (TO DO:Rename variables)

        Returns: 
            category_button -> hover over -> sub menu -> hover over -> sub menu category button -> click -> opens the sub menu category page 
        '''
        
        category_button = self.driver.find_element_by_xpath('//*[@id="chrome-sticky-header"]/div[2]/div[2]/nav/div/div/button[4]')
        self.a.move_to_element(category_button).perform()  #apply the hover over function on the category_button
        sub_categeory_button_clothing_new_in = self.driver.find_element_by_xpath('//*[@id="e87ba617-daa1-4b64-8f36-ab92e61283f7"]/div/div[2]/ul/li[1]/ul/li[2]/a') 
        self.a.move_to_element(sub_categeory_button_clothing_new_in).click().perform() #apply hover over and click functions on the sub_categ_button
        time.sleep(4)

        return category_button 

    def men_shopping_urls(self):

        ''' 
        # TODO: 
        # TODO: Code for clicking 'load more' button  
        # TODO: Find the element for the 'load more' button and click it. 
        '''
        product_container = self.driver.find_element_by_xpath('//*[@id="plp"]/div/div/div[2]/div/div[1]/section[1]') 
        product_list = product_container.find_elements_by_xpath('./article')
        
        
    def get_product_urls(self, other):
        self.product_urls = set([])
        for item in self.product_list:
            link = item.find_element_by_xpath('.//a').get_attribute('href')
        return self.product_urls.append(link)

        print(self.product_urls)
        print(len(self.product_urls))

    def load_next_page(self):
        next_page = []
        next_product_container = self.driver.find_element_by_xpath('//section[@id="plp"]/following-sibling::section') 
        next_page = next_product_container.find_elements_by_xpath('./article')

        #self.product_list += next_page

        # print(self.produc)
        #     next_page = self.driver.find_element_by_xpath("//section[@id='plp']/following-sibling::section")
            


        # TODO: refactor this into the code. 
        # It finds the next element in the section 
        # add the section tag <section /section>      //*[@id="plp"]/div/div/div[2]/div/div[1]/section[2]
                                                    #   //*[@id="plp"]/div/div/div[2]/div/div[1]/section[1]

        def _get_celebrity_list(self, date: str) -> list:
            # Add <ul> tags until you find the next <h2> tag
        next_node = self._get_birth_header(date)
        celebrities_list = []
        while True:
            next_node = next_node.find_next_sibling()
            if getattr(next_node, 'name') == 'ul':
                celebrities_list.extend(next_node.find_all('li'))
            elif getattr(next_node, 'name') == 'h2':
                break
        return celebrities_list
        
        
male_search = AsosScraper()
male_search.men_click_buttons() 
male_search.men_shopping_urls()