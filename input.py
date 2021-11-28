class UserInput():
    user_config = {                     #To scrape whole website set men + women = true, full options lists and 'products_per_category': 'max_value'
            'men':True,
            'women':True,
            'local':True,
            's3_bucket':False,
            'options_men':['Face + Body'],
#Options to choose from ['New in', 'Clothing', 'Shoes', 'Accessories', 'Topman', 'Sportswear', 'Face + Body']
            'options_women':['New in'],
#Options to choose from ['New in', 'Clothing', 'Shoes', 'Accessories', 'Topshop', 'Sportswear', 'Face + Body']
            'products_per_category': 2
            }
    
    gender_categories_dict = {} 
    def __init__(self):
        pass

     
 


    