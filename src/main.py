from blockutils import markdown_to_html_node
from mdutils import extract_title
import shutil
import os
import sys

basepath = "/" if len(sys.argv) <= 1 else sys.argv[1]

STATIC = "static"
PUBLIC = "docs"
CONTENT = "content"
TEMPLATE = "template.html"


def main():
    setup_public()


def setup_public():
    if os.path.exists(PUBLIC):
        shutil.rmtree(PUBLIC)
    os.mkdir(PUBLIC)
    copy_files(STATIC, PUBLIC, basepath)
    copy_files(CONTENT, PUBLIC, basepath)


def copy_files(src, dest, basepath=basepath):
    if os.path.exists(src):
        items = os.listdir(src)
        for item in items:
            src_str = os.path.join(src, item)
            dest_str = os.path.join(dest, item)
            if os.path.isfile(src_str):
                filename, ext = os.path.splitext(item)
                if ext == ".md":
                    dest_str = os.path.join(dest, filename + ".html")
                    generate_page(src_str, TEMPLATE, dest_str, basepath)
                else:
                    shutil.copy(src_str, dest_str)
            else:
                os.mkdir(dest_str)
                copy_files(src_str, dest_str)


def generate_page(from_path, template_path, dest_path, basepath=basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        md = f.read()

    title = extract_title(md)
    content = markdown_to_html_node(md).to_html()

    with open(template_path) as f:
        template = f.read()

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    with open(dest_path, "w") as f:
        f.write(template)


main()
