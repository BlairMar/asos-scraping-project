#%%
import random
import itertools

list1 = ['MIRUNA','MIRUNA','MIRUNA']
list2 = [1,2,3,4,5,6,7,8,9]
# list3 = random.sample(list2,4)
# print(list3)
# for i in (list2[0],list2[-1]):
    # print(i)
# def test_extract_links(self):
#     print(True if [str[:8] == 'https://' for str in self.links] else False)

# def test_extract_links():
#     print(True if [str[:4] == 'MIRU' for str in list1] else False)

# test_extract_links()
n = 3
for i, element in itertools.islice(enumerate(list2,1),n):
    
    print(i)
    # print(f'This is name {i}')

#%%
import random


def test_extract_links():
    self.scraper.driver.get("https://www.asos.com/men/new-in/cat/?cid=27110&nlid=mw|new+in|new+products|view+all")
    test_hrefs_list = random.sample(self.scraper.extract_links(
        '//*[@id="029c47b3-2111-43e9-9138-0d00ecf0b3db"]/div/div[2]/ul/li[1]/ul/li[*]', 2)
    for i in test_hrefs_list:
        href_click = i.click()
        return True
    self.assertTrue(href_click)

def test_extract_links():
    self.scraper.driver.get("https://www.asos.com/men/new-in/cat/?cid=27110&nlid=mw|new+in|new+products|view+all")
    test_hrefs_list = self.scraper.extract_links(
        '//*[@id="029c47b3-2111-43e9-9138-0d00ecf0b3db"]/div/div[2]/ul/li[1]/ul/li[*]', 2)
    for i in (test_hrefs_list[0],test_hrefs_list[-1])
        if test_hrefs_list[0]
    for i in test_hrefs_list:
        href_click = i.click()
        return True
    self.assertTrue(href_click)
        
    
#%%
def test_extract_links(self):
        self.scraper.driver.get("https://www.asos.com/men/new-in/cat/?cid=27110&nlid=mw|new+in|new+products|view+all")
        hrefs_list = self.scraper.extract_links('//*[@id="plp"]/div/div/div[2]/div/div[1]/section[1]/article')
        test_hrefs_list = random.sample(hrefs_list,2)
        for i in test_hrefs_list:
            # response = requests.get(i)
            # response = self.scraper.driver.get(i)
            # # print(response)
            # print(response.status_code)
            try:
                with urllib.request.urlopen(i) as f:
                   print(f.read())
                   print(f.status)
            except urllib.error.URLError as e:
                print(e.reason)

#%%
 def go_to_products(self):
        url_counter = 0
        for url in self.product_urls:  # TODO: use enumerate
            self.driver.get(url)
            url_counter += 1
            get_details(url_counter)

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
def get_details(self, url_counter):
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
               
def download_images(self):
         self.xpath_src_list = self.driver.find_elements_by_xpath('//*[@id="product-gallery"]/div[1]/div[2]/div[*]/img')
               self.src_list = []                                        
               for xpath_src in self.xpath_src_list:
                   self.src_list.append(xpath_src.get_attribute('src'))
        
               for i,src in enumerate(self.src_list[:-1]):   
                   urllib.request.urlretrieve(src, f"images\{self.gender}_Product{url_counter}.{i}.jpg")

print(self.product_information_dict)


product_search.go_to_products()

