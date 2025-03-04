import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is also a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_with_url(self):
        node = TextNode("This is a text node", TextType.LINK, "example.com")
        self.assertEqual(node.text, "This is a text node")
        self.assertEqual(node.text_type, TextType.LINK)
        self.assertEqual(node.url, "example.com")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        self.assertEqual(node.text, "This is a code node")
        self.assertEqual(node.text_type, TextType.CODE)
        self.assertEqual(node.url, None)


if __name__ == "__main__":
    unittest.main()
