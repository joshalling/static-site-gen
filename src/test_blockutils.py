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
        self.assertEqual(
            blockutils.split_block_of_type(
                "> Quote **BOLD**", blockutils.BlockType.QUOTE
            ),
            (None, "Quote **BOLD**"),
        )
        self.assertEqual(
            blockutils.split_block_of_type(
                "- unordered list item", blockutils.BlockType.UNORDERED_LIST
            ),
            (None, "unordered list item"),
        )
        self.assertEqual(
            blockutils.split_block_of_type(
                "123. ordered list item", blockutils.BlockType.ORDERED_LIST
            ),
            (None, "ordered list item"),
        )
        self.assertEqual(
            blockutils.split_block_of_type(
                "```this is some preformatted code```", blockutils.BlockType.CODE
            ),
            (None, "this is some preformatted code"),
        )
        self.assertEqual(
            blockutils.split_block_of_type(
                "This is a paragraph of text with a line brea.\nThis is after the line break",
                blockutils.BlockType.PARAGRAPH,
            ),
            (
                None,
                "This is a paragraph of text with a line brea.\nThis is after the line break",
            ),
        )

    def test_block_to_html_heading(self):
        block = "##### This is a _small_ heading with `code` in it"
        result = blockutils.block_to_html(block)

        self.assertEqual(
            "<h5>This is a <i>small</i> heading with <code>code</code> in it</h5>",
            result,
        )

    def test_block_to_html_ordered_list(self):
        block = "1. ordered **item** 1\n1. _ordered_ item 2"
        result = blockutils.block_to_html(block)

        self.assertEqual(
            "<ol><li>ordered <b>item</b> 1</li><li><i>ordered</i> item 2</li></ol>",
            result,
        )

    def test_block_to_html_unordered_list(self):
        block = "- ordered **item** 1\n- _ordered_ item 2"
        result = blockutils.block_to_html(block)

        self.assertEqual(
            "<ul><li>ordered <b>item</b> 1</li><li><i>ordered</i> item 2</li></ul>",
            result,
        )

    def test_block_to_html_code(self):
        block = """```
        // This **is** _some_ preformatted code
        def funky_func():
            pass
        ```"""
        result = blockutils.block_to_html(block)

        self.assertEqual(
            """<pre>
        // This **is** _some_ preformatted code
        def funky_func():
            pass
        </pre>""",
            result,
        )

    def test_block_to_html_quote(self):
        block = "> This is a quote\n> on two lines"
        result = blockutils.block_to_html(block)

        self.assertEqual(
            "<blockquote>This is a quote on two lines</blockquote>",
            result,
        )

    def test_block_to_html_paragraph(self):
        block = "This is a **long** paragraph\nwith multiple lines of text."
        result = blockutils.block_to_html(block)

        self.assertEqual(
            "<p>This is a <b>long</b> paragraph with multiple lines of text.</p>",
            result,
        )

    def test_markdown_to_html(self):
        markdown = """# Heading 1

This is a description but we added some **bold** and _italic_ words.

## This is the first subheading

```
// we should include some code
def my_func():
    print("do something")
```

- item 1
- item `2`

1. numbered 1
2987987. _numbered_ 2

> This is a blockquote
> with 2 lines
"""
        result = blockutils.markdown_to_html(markdown)

        expected = '<div><h1>Heading 1</h1><p>This is a description but we added some <b>bold</b> and <i>italic</i> words.</p><h2>This is the first subheading</h2><pre>\n// we should include some code\ndef my_func():\n    print("do something")\n</pre><ul><li>item 1</li><li>item <code>2</code></li></ul><ol><li>numbered 1</li><li><i>numbered</i> 2</li></ol><blockquote>This is a blockquote with 2 lines</blockquote></div>'

        self.assertEqual(result, expected)
