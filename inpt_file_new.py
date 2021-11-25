from ASOS_Scraper_updated import AsosScraper
from selenium import webdriver


class User_input(AsosScraper):
    driver = webdriver.Chrome()
    gender_dict = {}
    

    def __init__(self):
        self.gender = ""
        self.location = ""
    
    options_men, options_women = AsosScraper.get_categories_options_from_ASOS
    print(options_men,options_women)
    
        
    print('Welcome to the ASOS webscraper!')
    def S3_bucket_or_local_machine(self):
        answer_locally = input('Do you want to save the data to your local machine?[y/n]')
        answer_s3_bucket = input('Do you want to save the data to a public S3_bucket?[y/n]')
        while True:
            if answer_locally == 'y' and answer_s3_bucket == 'n':
                self.location = 'local_machine'
                return self.location 
            elif answer_locally == 'n' and answer_s3_bucket == 'y':
                self.location = 's3_bucket'
                return self.location
            elif answer_locally == 'y' and answer_s3_bucket == 'y':
                self.location = 'local_machine & s3_bucket'
                return self.location
            else:
                print('Invalid input. Please choose again!')
                answer_locally = input('Do you want to save the data to your local machine?[y/n]')
                answer_s3_bucket = input('Do you want to save the data to a public S3_bucket?[y/n]')

    def scrape_or_not(self):
        answer = input('Do you want to scrape the whole website? [y/n]: ')
        if answer == 'y':
            self.scrape_all_website()
        if answer == 'n':
            self.m = input('Do you want to scrape the men section?[y/n]')
            self.w = input('Do you want to scrape the women section?[y/n]')

            if self.m == 'y' and self.w == 'y':
                self.men_yes_women_yes()
            
            elif self.m == 'n' and self.w == 'n':
                self.men_no_women_no()
        
            elif self.m == 'y' and self.w == 'n':
                self.men_yes_women_no()
        
            elif self.m == 'n' and self.w == 'y':
                self.men_no_women_yes()

            else: 
                print('Invalid answers. Please choose a valid answer!')
                self.scrape_or_not()
        self.S3_bucket_or_local_machine()

    def men_no_women_no(self):
        answer = input('No gender chosen. Do you wish to exit? [y/n]: ')   
        while True:
            if answer == 'y':
                exit()
            elif answer == 'n':
                self.scrape_or_not()
            else:
                print('Invalid input. Please choose again!')
                answer = input('No gender chosen. Do you wish to exit? [y/n]: ')
            
    def men_yes_women_no(self):
        self.gender = 'men'
        self.gender_categories(self.gender)

    def men_no_women_yes(self): 
        self.gender = 'women'
        self.gender_categories(self.gender)

    def men_yes_women_yes(self):
        self.gender_categories()
    
    def gender_categories(self, gender = None):
        self.men_categories_list = []
        self.women_categories_list = []
        if gender == 'men':
            print('Choose from men\'s categories')
            self.men_categories_list = self.choose_category(self.options_men) 
            self.gender_dict.update(self.addItemToDictionary(gender, 2, self.men_categories_list))

        elif gender == 'women': 
            print('Choose from women\'s categories')
            self.women_categories_list = self.choose_category(self.options_women)
            self.gender_dict.update(self.addItemToDictionary(gender, 1, self.women_categories_list))

        else:
            print('Choose from men\'s categories')
            gender = 'men'
            self.men_categories_list = self.choose_category(self.options_men) 
            self.gender_dict.update(self.addItemToDictionary(gender, 2, self.men_categories_list))
            print('Choose from women\'s categories')
            gender = 'women'
            self.women_categories_list = self.choose_category(self.options_women)
            self.gender_dict.update(self.addItemToDictionary(gender, 1, self.women_categories_list))
            print(self.men_categories_list,self.women_categories_list)
        print(self.gender_dict)
        self.products_per_category = int(input('How many products per category? Introduce a number: '))
        print(f'You will scrape a total of {self.total_number_of_products(self.products_per_category)} products')
        return self.gender_dict 

    def total_number_of_products(self, products_per_category):
        total_of_products = (len(self.men_categories_list) + len(self.women_categories_list)) * products_per_category
        return total_of_products

    def addItemToDictionary(self, gender:str, gender_index: int, categories_list:list):
        gender_dict = {gender:[gender_index,categories_list]}
        return gender_dict
 
    def scrape_all_website(self):
        gender = 'men'
        self.gender_dict.update(self.addItemToDictionary(gender, 2, self.options_men))
        gender = 'women'
        self.gender_dict.update(self.addItemToDictionary(gender, 1, self.options_women))
        # print(self.gender_dict)
        return self.gender_dict
        


    def choose_category(self, options:list):
        categories_choice = []
        for category in options:
            choice = input(f'{category}? [y/n]: ')
            # number_of_products = int(input(f'How many products from {category}? ')
            while True:
                if choice == 'y':
                    categories_choice.append(category)
                    break
                elif choice == 'n':
                    break 
                else:
                    print('Invalid answer. Please choose again!')
                    choice = input(f'{category}? [y/n]: ')
        return categories_choice
            

instance_choices = User_input()
instance_asos = AsosScraper()
# instance_choices.scrape_or_not()