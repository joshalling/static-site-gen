import unittest

import blockutils


class TestBlockUtils(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = blockutils.markdown_to_blocks(md)
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
        blocks = blockutils.markdown_to_blocks(md)
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
        type = blockutils.block_to_blocktype(block)

        self.assertEqual(type, blockutils.BlockType.HEADING)

    def test_block_to_block_type_heading_invalid(self):
        block = """####### Heading"""
        type = blockutils.block_to_blocktype(block)

        self.assertEqual(type, blockutils.BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list(self):
        block = """- item1\n- item2\n- item3"""
        type = blockutils.block_to_blocktype(block)

        self.assertEqual(type, blockutils.BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_invalid(self):
        block = """- item1\n-item2\n- item3"""
        type = blockutils.block_to_blocktype(block)

        self.assertEqual(type, blockutils.BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list(self):
        block = """1. item1\n1. item2\n1. item3"""
        type = blockutils.block_to_blocktype(block)

        self.assertEqual(type, blockutils.BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_invalid(self):
        block = """1. item1\n1 item2\n1. item3"""
        type = blockutils.block_to_blocktype(block)

        self.assertEqual(type, blockutils.BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        block = """```code
        is
        cool```"""
        type = blockutils.block_to_blocktype(block)

        self.assertEqual(type, blockutils.BlockType.CODE)

    def test_block_to_block_type_code_invalid(self):
        block = """```code
        is
        cool``"""
        type = blockutils.block_to_blocktype(block)

        self.assertEqual(type, blockutils.BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        block = """> quote1\n> quote2\n> quote3"""
        type = blockutils.block_to_blocktype(block)

        self.assertEqual(type, blockutils.BlockType.QUOTE)

    def test_block_to_block_type_quote_invalid(self):
        block = """> quote1\n- quote2\n> quote3"""
        type = blockutils.block_to_blocktype(block)

        self.assertEqual(type, blockutils.BlockType.PARAGRAPH)

    def test_split_block_of_type(self):
        self.assertEqual(
            blockutils.split_block_of_type("### Head", blockutils.BlockType.HEADING),
            ("###", "Head"),
        )

    def test_block_to_html_heading(self):
        block = "##### This is a _small_ heading with `code` in it"
        result = blockutils.block_to_html(block)

        self.assertEqual(
            "<h5>This is a <i>small</i> heading with <code>code</code> in it</h5>",
            result,
        )
