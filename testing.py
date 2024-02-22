import json
import unittest
import warnings
from io import StringIO
from unittest.mock import patch
from typing import List
from pydantic import BaseModel
import main  # assuming main module contains the 'main' function


# Pydantic model for test data
class TestData(BaseModel):
    test_name: str
    input_data: List[int]
    output_data: List[int]


# Function to load test data from a JSON file and validate using the Pydantic model
def load_test_data(file_path: str) -> List[TestData]:
    with open(file_path, "r") as file:
        json_data_list = json.load(file)
    # Validate each item in the loaded JSON data using the Pydantic model
    return [TestData.model_validate(item) for item in json_data_list]


# Test class for the main program
class TestMainProgram(unittest.TestCase):
    # Class method to set up common data for all test methods in the test class
    @classmethod
    def setUpClass(cls):
        # Load test data from the "tests.json" file before running any tests
        cls.test_data_list = load_test_data("tests.json")

    # Method to set up common data for each test method in the test class
    def setUp(self):
        # Create a StringIO object to capture the standard output
        self.mock_stdout = StringIO()

    # Method to tear down common data after each test method in the test class
    def tearDown(self):
        # Close the StringIO object to clean up resources
        self.mock_stdout.close()

    # Test method to check the main program's behavior with invalid input
    def test_process_numbers_invalid_input(self):
        # Iterate over each test case in the loaded test data
        for test in self.test_data_list:
            # Use self.subTest for better test isolation and identification
            with self.subTest(test_name=test.test_name):
                # Patch 'input' and 'sys.stdout' for capturing and mocking input/output
                with patch("builtins.input", side_effect=test.input_data), \
                        patch("sys.stdout", new_callable=StringIO) as self.mock_stdout, \
                        warnings.catch_warnings(record=True) as caught_warnings:
                    # Run the 'main' function to simulate program execution
                    main.main()

                    # Extract actual output data from the captured standard output
                    actual_output_data = [int(s.strip()[-1]) for s in self.mock_stdout.getvalue().strip().split("\n")
                                          if s.startswith("participant")]

                    # Assert that the actual output matches the expected output from the test data
                    self.assertEqual(actual_output_data, test.output_data)

                    # Output any warnings captured during the test
                    for warning in caught_warnings:
                        print(warning.message)


# Entry point for running the unit tests
if __name__ == "__main__":
    unittest.main()
