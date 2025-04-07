import unittest
from conformal_hulls.core import example_function

class TestCore(unittest.TestCase):
    def test_example_function(self):
        self.assertEqual(example_function(), "Hello, Conformal Hulls!")

if __name__ == "__main__":
    unittest.main()