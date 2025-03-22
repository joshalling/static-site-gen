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


heading_regex = r"^#{1,6} "
olist_regex = r"^\d+\. "


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return list(
        filter(lambda block: block != "", map(lambda block: block.strip(), blocks))
    )


def block_to_blocktype(block):
    lines = block.split("\n")
    if len(lines) == 1 and re.match(heading_regex, block):
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
            prefix = re.findall(heading_regex, block)[0]
            return block[: len(prefix) - 1], block[len(prefix) :]
        case BlockType.UNORDERED_LIST:
            return None, block[2:]
        case BlockType.ORDERED_LIST:
            prefix = re.findall(olist_regex, block)[0]
            return None, block[len(prefix) :]
        case BlockType.CODE:
            return None, block[3 : len(block) - 3]
        case BlockType.QUOTE:
            return None, block[2:]
        case BlockType.PARAGRAPH:
            return None, block


def blocktype_to_html_tag(blocktype, prefix):
    match blocktype:
        case BlockType.HEADING:
            return f"h{len(prefix)}"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
        case BlockType.CODE:
            return "pre"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.PARAGRAPH:
            return "p"


def get_block_meta(block, blocktype):
    prefix, text = split_block_of_type(block, blocktype)

    textnodes = inlineutils.text_to_text_nodes(text)
    inner = "".join(
        map(
            lambda node: inlineutils.text_node_to_html_node(node).to_html(),
            textnodes,
        )
    )
    tag = blocktype_to_html_tag(blocktype, prefix)

    return inner, tag


def block_to_html(block):
    blocktype = block_to_blocktype(block)
    html_lines = []
    tag = None
    if blocktype == BlockType.HEADING:
        inner, tag = get_block_meta(block, blocktype)
        html_lines.append(inner)
    elif blocktype == BlockType.CODE:
        prefix, text = split_block_of_type(block, blocktype)
        tag = blocktype_to_html_tag(blocktype, prefix)
        html_lines.append(text)
    else:
        lines = block.split("\n")
        for line in lines:
            inner, tag = get_block_meta(line, blocktype)
            if (
                blocktype == BlockType.ORDERED_LIST
                or blocktype == BlockType.UNORDERED_LIST
            ):
                html_lines.append(f"<li>{inner}</li>")
                continue
            html_lines.append(inner)
    delimiter = " " if blocktype in [BlockType.QUOTE, BlockType.PARAGRAPH] else ""

    return f"<{tag}>{delimiter.join(html_lines)}</{tag}>"


def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    html_blocks = list(map(lambda block: block_to_html(block), blocks))
    return f"<div>{"".join(html_blocks)}</div>"
