def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return list(map(lambda block: block.strip(), blocks))
