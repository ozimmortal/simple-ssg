from unittest import TestCase
from src.utils.helper_functions import *

class TestHelperFunctions(TestCase):

    def test_extract_title(self):

        md = """
# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.
"""
        title = extract_title(md)
        self.assertEqual(title , "Tolkien Fan Club")
    
    def test_extract_title_with_no_title(self):
        md = "hello"

        with self.assertRaises(Exception):
            extract_title(md)

