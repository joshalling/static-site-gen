import unittest
import mdutils


class TestMdUtils(unittest.TestCase):
    def test_extract_title(self):
        title = mdutils.extract_title("# Hello world!\n\nThis is my blog post")

        self.assertEqual(title, "Hello world!")

    def test_extract_title_untitled(self):
        title = mdutils.extract_title("Hello world!\n\nThis is my blog post")

        self.assertEqual(title, "Untitled")
