# from ASOS_Scraper import AsosScraper

class User_input():
    def __init__(self):
        self.options_men = ['New in', 'Clothing', 'Shoes', 'Accessories', 'Topman', 'Sportswear', 'Face+Body', 'Outlet']
        self.options_women = ['New in', 'Clothing', 'Shoes', 'Accessories', 'Topshop', 'Sportswear', 'Face+Body', 'Outlet']
        self.gender = str
        self.gender_dict = {}
    print('Welcome to the ASOS webscraper')
    # print('Introduce the gender and the category name and I will give you the products details and images')
    # print('But first, where would you like to store the information? On your local machine or in a public AWS S3 bucket?')
    # location = str(input('For "local machine" choose 1, for "S3 bucket" choose 2: '))
    # gender = str(input('Introduce the gender: ')) 

    def scrape_or_not(self):
        answer = input('Do you want to scrape the whole website? [y/n]: ')
        if answer == 'y':
            print('method to scrape all categories') 
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


    def men_no_women_no(self):
        answer = input('No gender chosen. Do you wish to exit? [y/n]: ')   
        if answer == 'y':
            exit()
        
        elif self.answer == 'n':
            self.scrape_or_not()
        else:
            print('Invalid input. Please choose again!')
            self.men_no_women_no()

    def men_yes_women_no(self):
        self.gender = 'men'
        self.gender_categories(self.gender)

    def men_no_women_yes(self): 
        self.gender = 'women'
        self.gender_categories(self.gender)

    def men_yes_women_yes(self):
        self.gender_categories()
    
    def gender_categories(self, gender = None):
        # self.gender_dict = {}
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
        return self.gender_dict     
        
    def addItemToDictionary(self, gender:str, gender_index: int, categories_list:list):
        gender_dict = {gender:[gender_index,categories_list]}
        return gender_dict
 

    def choose_category(self, options:list):
        categories_choice = []
        for category in options:
            choice = input(f'{category}? [y/n]: ')
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
            
# instance_choices = User_input()
# instance_choices.scrape_or_not()














    
#     category_list = list(map(str,
#     input('Choose one or more categories within the following list: New in, Clothing, Shoes, Accessories, Topshop, Sportswear, Face+Body, Outlet').split()))
# category_name = list(map(str, input("Introduce one or more categories: ").split()))
# number_of_products = int(input('How many products do you want to get details for? '))


                                     
# if __name__ == '__main__':
#     product_search = AsosScraper(webdriver.Chrome, gender,number_of_products,location, categories:list)
#     product_search.click_buttons('//*[@id="chrome-header"]/header/div[1]/div/div/button', 1) #this xpath is for accepting the cookies                         
#     product_search.primary_method()
#     product_search.driver.quit()