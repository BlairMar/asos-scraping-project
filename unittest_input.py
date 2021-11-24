import unittest 
from input_file import User_input

class User_Input_Tests(unittest.TestCase):

    def setUp(self):
        self.input = User_input()

    def test_scrape_or_not(self):
        # Sample input 
        # Run instance of class against scrape_or_not method 
        sample_input = self.input.scrape_or_not()
        # When program runs, test whether the expected outputs work
        expected_outputs = ['y', 'n', int]
        # if input correctly, return True
        self.assertTrue(sample_input, expected_outputs)


    def test_gender_categories(self):
        actual_value = self.input.gender_categories()
        print(type(actual_value))
        self.assertIsInstance(actual_value, dict) 

    # def test_total_number_of_products(self):
    #     self.input.total_number_of_products(7)
    #     expected_output = 20
    #     self.assertEqual(expected_output)        
         
    def tearDown(args):
        pass 

unittest.main(argv=[''], verbosity=2, exit=False)
