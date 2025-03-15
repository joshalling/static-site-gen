from textnode import TextType, TextNode
from leafnode import LeafNode
import re


def text_node_to_html_node(textnode):
    match textnode.text_type:
        case TextType.BOLD:
            return LeafNode("b", textnode.text)
        case TextType.ITALIC:
            return LeafNode("i", textnode.text)
        case TextType.CODE:
            return LeafNode("code", textnode.text)
        case TextType.LINK:
            return LeafNode("a", textnode.text, props={"href": textnode.url})
        case TextType.IMAGE:
            return LeafNode(
                "img", "", props={"src": textnode.url, "alt": textnode.text}
            )
        case _:
            return LeafNode(None, textnode.text)


def split_nodes_delimiter(nodes, delimiter, text_type):
    new_nodes = []
    for node in nodes:
        text_list = node.text.split(delimiter)
        for i in range(len(text_list)):
            type = i % 2 == 1 and text_type or node.text_type
            new_nodes.append(TextNode(text_list[i], type))
    return new_nodes


def split_nodes_image(nodes):
    new_nodes = []
    for node in nodes:
        images = extract_markdown_images(node.text)
        if len(images) > 0:
            text_to_use = node.text
            for alt, url in images:
                text_list = text_to_use.split(f"![{alt}]({url})", 1)
                new_nodes.append(TextNode(text_list[0], node.text_type))
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                text_to_use = text_list[1]

        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
