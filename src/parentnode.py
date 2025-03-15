from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode tag cannot be empty")

        if self.children is None:
            raise ValueError("ParentNode children cannot be empty")

        return (
            f"<{self.tag}{self.props_to_html()}>{self.children_to_html()}</{self.tag}>"
        )

    def children_to_html(self):
        return "".join([child.to_html() for child in self.children])
