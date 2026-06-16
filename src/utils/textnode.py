from enum import Enum
from .htmlnode import *
import re


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: "str|None" = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):

        if (
            self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url
        ):
            return True

        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unknown Text Type: {text_node.text_type}")


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:

    new_nodes = []
    pattern = f"{re.escape(delimiter)}(.*?){re.escape(delimiter)}"
    for old_node in old_nodes:

        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        if old_node.text.count(delimiter) % 2 != 0:
            raise ValueError("Invalid markdown syntax")

        start, length = 0, len(old_node.text)

        for match in re.finditer(pattern, old_node.text):
            inline_start, inline_end = match.start(), match.end()
            inline_text = match.group(1)
            normal_text = old_node.text[start:inline_start]

            if normal_text:
                new_nodes.append(TextNode(normal_text, TextType.TEXT))

            new_nodes.append(TextNode(inline_text, text_type))
            start = inline_end

        if start < length:
            new_nodes.append(TextNode(old_node.text[start:], TextType.TEXT))

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str]]:
    pattern = r"\!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> list[tuple[str]]:
    pattern = r"\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    
    new_nodes = []
    pattern = r"\!\[(.*?)\]\((.*?)\)"
    for old_node in old_nodes:

        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        start, length = 0, len(old_node.text)

        for match in re.finditer(pattern, old_node.text):
            inline_start, inline_end = match.start(), match.end()
            alt, url = match.group(1) , match.group(2)
            normal_text = old_node.text[start:inline_start]

            if normal_text:
                new_nodes.append(TextNode(normal_text, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            start = inline_end

        if start < length:
            new_nodes.append(TextNode(old_node.text[start:], TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    for old_node in old_nodes:

        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        start, length = 0, len(old_node.text)

        for match in re.finditer(pattern, old_node.text):
            inline_start, inline_end = match.start(), match.end()
            alt, url = match.group(1) , match.group(2)
            normal_text = old_node.text[start:inline_start]

            if normal_text:
                new_nodes.append(TextNode(normal_text, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.LINK, url))
            start = inline_end

        if start < length:
            new_nodes.append(TextNode(old_node.text[start:], TextType.TEXT))

    return new_nodes

def text_to_textnodes(text:str) -> list[TextNode]:
    node = TextNode(text , TextType.TEXT)
    return split_nodes_link(
            split_nodes_image(split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(
                        [node] , "**" , TextType.BOLD)
                        , "_" , TextType.ITALIC) , "`" , TextType.CODE)))



