from textnode import TextType
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
