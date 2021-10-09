    '''
    Function to get the Selenium package to click the 'accept cookies' 
    button 

    Attributes: 
        driver  

    Returns
        selenium webelement which clicks on the accept cookies button

    '''
    
    # To be added as a method inside the AsosScraper Class 

    
    def accept_cookies_button(self):
        time.sleep(4)
        click_accept_cookies = self.driver.find_element_by_xpath('//button[@class="g_k7vLm _2pw_U8N _2BVOQPV"]')
        click_accept_cookies.click()


