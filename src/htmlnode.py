class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, attributes=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.attributes = attributes

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        attrs = ""

        for key, value in self.attributes.items():
            attrs += f' {key}="{value}"'

        return attrs
