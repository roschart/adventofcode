import unittest

from day01 import get_data_from_file, calculate_distance, similarity

class TestCalculateDistance(unittest.TestCase):
    def test_example(self):
        file_path = "../test" 
        expected_result = 11

        # Read and process the test file
        col1, col2 = get_data_from_file(file_path)

        # Calculate the result
        result = calculate_distance(col1, col2)

        # Assert the expected result
        self.assertEqual(result, expected_result)

class TestCalculateSimilarity(unittest.TestCase):
    def test_example(self):
        file_path = "../test" 
        expected_result = 31

        # Read and process the test file
        col1, col2 = get_data_from_file(file_path)

        # Calculate the result
        result = similarity(col1, col2)

        # Assert the expected result
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()