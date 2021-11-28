class UserInput():
    user_config = {                     #To scrape whole website set men + women = true, full options lists and 'products_per_category': 'max_value'
            'men':False,
            'women':True,
            'local':False,
            's3_bucket':True,
            'options_men':['Topman', 'Sportswear', 'Face + Body'],
#Options to choose from ['New in', 'Clothing', 'Shoes', 'Accessories', 'Topman', 'Sportswear', 'Face + Body']
            'options_women':['New in', 'Clothing', 'Shoes', 'Accessories'],
#Options to choose from ['New in', 'Clothing', 'Shoes', 'Accessories', 'Topshop', 'Sportswear', 'Face + Body']
            'products_per_category': 5
            }
    
    configuration = {}
    location = []
    
    
    
    def __init__(self):
        # self.user_config = user_config
        pass
    
    def scraper_config(self):
        if self.user_config['men'] == True:
            gender_index = 2
            categories = self.user_config['options_men']     
            self.configuration.update(self.add_item_to_dictionary('men', gender_index, categories))

        if self.user_config['women'] == True:
            gender_index = 1
            categories = self.user_config['options_women']      
            self.configuration.update(self.add_item_to_dictionary('women', gender_index, categories))
    
        print(self.configuration)

    def add_item_to_dictionary(self, gender:str, gender_index: int, categories:list):
        configuration = {gender:[gender_index,categories]}
        return configuration
     
    def location_config(self):
        if self.user_config.get('local') == True:
            self.location.append('local')

        if self.user_config.get('s3_bucket') == True:
            self.location.append('s3_bucket')
        print(self.location)

config1 = UserInput()
config1.scraper_config()
config1.location_config()
print(config1.user_config.get('products_per_category'))
    