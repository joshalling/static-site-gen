from textnode import TextType, TextNode
from leafnode import LeafNode


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
