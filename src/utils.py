from textnode import TextType, TextNode
from leafnode import LeafNode
import re

type_to_delimeter = {
    TextType.BOLD: "**",
    TextType.ITALIC: "_",
    TextType.CODE: "`",
}


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
            if len(text_to_use) > 0:
                new_nodes.append(TextNode(text_to_use, node.text_type))

        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_link(nodes):
    new_nodes = []
    for node in nodes:
        links = extract_markdown_links(node.text)
        if len(links) > 0:
            text_to_use = node.text
            for text, url in links:
                text_list = text_to_use.split(f"[{text}]({url})", 1)
                new_nodes.append(TextNode(text_list[0], node.text_type))
                new_nodes.append(TextNode(text, TextType.LINK, url))
                text_to_use = text_list[1]
            if len(text_to_use) > 0:
                new_nodes.append(TextNode(text_to_use, node.text_type))

        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)


def text_to_text_nodes(text):
    parent_node = TextNode(text, TextType.TEXT)
    nodes = [parent_node]
    for type in TextType:
        if type in type_to_delimeter:
            nodes = split_nodes_delimiter(nodes, type_to_delimeter[type], type)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
