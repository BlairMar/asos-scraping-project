import unittest 
from input_file import User_input


class User_Input_Tests(unittest.TestCase):

    def setUp(self):
        self.input = User_input()
     

    # Successful Unittest! 

    def test_scrape_or_not(self):
        # Sample input 
        # Run instance of class against scrape_or_not method 
        sample_input = self.input.scrape_or_not()
        # When program runs, test whether the expected outputs work
        expected_outputs = ['y', 'n', int]
        # if input correctly, return True
        self.assertTrue(sample_input, expected_outputs)

    # Successful Unittest 

    def test_gender_categories(self):
        actual_value = self.input.gender_categories()
        print(type(actual_value))
        self.assertIsInstance(actual_value, dict) 

    
    # Sucessful Unittest ! 

    def test_addItemToDictionary(self):
        # testing if the dictionary is returned from the method 
        test_input = self.input.addItemToDictionary('men', 2, categories_list=list)
        self.assertIsInstance(test_input, dict) 
     
    #   # Successful Unittest ! 
    
    def test_choose_category(self):
        # testing if a list is returned from the method 
        options = ['New in', 'Clothing', 'Shoes', 'Accessories', 'Topman', 'Sportswear', 'Face+Body']
        self.input.choose_category(options)
        self.assertIsInstance(options, list)    

    # Successful Unittest ! 

    def test_scrape_all_website(self):
        # testing if a dictionary is returned from the method
        sample_scraper = self.input.scrape_all_website()
        self.assertIsInstance(sample_scraper, dict)
    
    # Successful Unittest ! 

    def test_save_to_local_machine_or_s3(self):
        # testing whether the the output returns a string from the method
        test_input  = self.input.S3_bucket_or_local_machine()
        self.assertIsInstance(test_input, str)

    # Successful Unittest ! 

    def test_total_number_of_products(self):
        # Run input through geneder_categories method 
        self.input.gender_categories()
        # select 'yes' to each 
        # 2 represents the number of products_per_category
        test_input = self.input.total_number_of_products(2)
        # There are 14 categories therefore 14 * 2 = 28 
        expected_output = 28
        self.assertEqual(test_input, expected_output)
      
    def tearDown(args):
        pass 

unittest.main(argv=[''], verbosity=2, exit=False)
