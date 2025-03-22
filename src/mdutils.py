import re


def extract_title(md):
    title = re.findall(r"# (.*)", md)
    if len(title) > 0:
        return title[0]
    return "Untitled"
