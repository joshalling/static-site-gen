import unittest

from blockutils import markdown_to_blocks, block_to_blocktype, BlockType


class TestBlockUtils(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        block = """### Heading"""
        type = block_to_blocktype(block)

        self.assertEqual(type, BlockType.HEADING)

    def test_block_to_block_type_heading_invalid(self):
        block = """####### Heading"""
        type = block_to_blocktype(block)

        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list(self):
        block = """- item1\n- item2\n- item3"""
        type = block_to_blocktype(block)

        self.assertEqual(type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_invalid(self):
        block = """- item1\n-item2\n- item3"""
        type = block_to_blocktype(block)

        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list(self):
        block = """1. item1\n1. item2\n1. item3"""
        type = block_to_blocktype(block)

        self.assertEqual(type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_invalid(self):
        block = """1. item1\n1 item2\n1. item3"""
        type = block_to_blocktype(block)

        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        block = """```code
        is
        cool```"""
        type = block_to_blocktype(block)

        self.assertEqual(type, BlockType.CODE)

    def test_block_to_block_type_code_invalid(self):
        block = """```code
        is
        cool``"""
        type = block_to_blocktype(block)

        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        block = """> quote1\n> quote2\n> quote3"""
        type = block_to_blocktype(block)

        self.assertEqual(type, BlockType.QUOTE)

    def test_block_to_block_type_quote_invalid(self):
        block = """> quote1\n- quote2\n> quote3"""
        type = block_to_blocktype(block)

        self.assertEqual(type, BlockType.PARAGRAPH)
