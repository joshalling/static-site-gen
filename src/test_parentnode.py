import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_parent_with_no_children(self):
        node = ParentNode("div")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_with_no_tag(self):
        node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_children_without_tag(self):
        child_node_1 = LeafNode(None, "child 1")
        child_node_2 = LeafNode("span", "child 2")
        parent_node = ParentNode("div", [child_node_1, child_node_2])
        self.assertEqual(
            parent_node.to_html(), "<div>child 1<span>child 2</span></div>"
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
