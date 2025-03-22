from enum import Enum
import re

import inlineutils


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    UNORDERED_LIST = "ulist"
    ORDERED_LIST = "olist"
    CODE = "code"
    QUOTE = "quote"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return list(
        filter(lambda block: block != "", map(lambda block: block.strip(), blocks))
    )


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


def split_block_of_type(block, blocktype):
    match blocktype:
        case BlockType.HEADING:
            prefix = re.findall(r"^#{1,6} ", block)[0]
            return block[: len(prefix) - 1], block[len(prefix) :]


def blocktype_to_html_tag(blocktype, prefix):
    match blocktype:
        case BlockType.HEADING:
            return f"h{len(prefix)}"


def block_to_html(block):
    blocktype = block_to_blocktype(block)
    prefix, text = split_block_of_type(block, blocktype)

    textnodes = inlineutils.text_to_text_nodes(text)
    inner = "".join(
        map(lambda node: inlineutils.text_node_to_html_node(node).to_html(), textnodes)
    )
    tag = blocktype_to_html_tag(blocktype, prefix)

    return f"<{tag}>{inner}</{tag}>"
