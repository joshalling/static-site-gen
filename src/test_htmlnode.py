import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode("div", "Hello")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_to_html(self):
        node = HTMLNode("div", "Hello")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode("div", "Hello", props={"class": "test", "id": "test"})
        self.assertEqual(node.props_to_html(), ' class="test" id="test"')
