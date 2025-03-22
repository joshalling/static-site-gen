from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    UNORDERED_LIST = "ulist"
    ORDERED_LIST = "olist"
    CODE = "code"
    QUOTE = "quote"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return list(map(lambda block: block.strip(), blocks))


def block_to_blocktype(block):
    lines = block.split("\n")
    if len(lines) == 1 and re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    elif all(re.match(r"^\d+\. ", line) for line in lines):
        return BlockType.ORDERED_LIST
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    else:
        return BlockType.PARAGRAPH
