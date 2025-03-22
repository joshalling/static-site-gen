from textnode import TextNode, TextType
import shutil
import os

SRC = "static"
DEST = "public"


def main():
    setup_public()


def setup_public():
    if os.path.exists(DEST):
        shutil.rmtree(DEST)

    os.mkdir(DEST)
    copy_files(SRC, DEST)


def copy_files(src, dest):
    if os.path.exists(src):
        items = os.listdir(src)
        for item in items:
            src_str = os.path.join(src, item)
            dest_str = os.path.join(dest, item)
            if os.path.isfile(src_str):
                shutil.copy(src_str, dest_str)
            else:
                os.mkdir(dest_str)
                copy_files(src_str, dest_str)


main()
