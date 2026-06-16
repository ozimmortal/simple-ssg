from enum import Enum
from .htmlnode import *
from .textnode import *
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:

    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in block.split("\n")):
        return BlockType.QUOTE

    if all(line.startswith(("- ", "* ")) for line in block.split("\n")):
        return BlockType.UNORDERED_LIST

    if all(re.match(rf"^{i+1}\. ", line) for i, line in enumerate(block.split("\n"))):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown: str) -> list[str]:
    return [block.strip() for block in markdown.strip().split("\n\n") if block.strip()]


def block_to_html_node(block: str) -> ParentNode:

    block_type = block_to_block_type(block)
    if block_type == BlockType.CODE:
        code = block.strip("`").lstrip()
        return ParentNode("pre", [LeafNode("code", code)])

    if block_type == BlockType.HEADING:
        marker, text = block.split(" " , 1)
        text_nodes = text_to_textnodes(text)
        leaf_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
        level = len(marker)
        parent_node = ParentNode(f"h{level}", leaf_nodes)
        
        return parent_node

    if block_type == BlockType.QUOTE:
        stripped = "\n".join(line.lstrip(">").lstrip(" ") for line in block.split("\n"))
        text_nodes = text_to_textnodes(stripped.replace("\n", " "))
        leaf_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
        parent_node = ParentNode("blockquote", leaf_nodes)

        return parent_node

    if block_type == BlockType.UNORDERED_LIST:
        items = []

        for line in block.split("\n"):
            text_nodes = text_to_textnodes(line[2:])
            leaf_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
            parent_node = ParentNode("li", leaf_nodes)

            items.append(parent_node)

        return ParentNode("ul", items)

    if block_type == BlockType.ORDERED_LIST:
        items = []

        for line in block.split("\n"):
            text_nodes = text_to_textnodes(re.sub(r"^\d+\. ", "", line))
            leaf_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
            parent_node = ParentNode("li", leaf_nodes)

            items.append(parent_node)

        return ParentNode("ol", items)

    # paragraph

    text_nodes = text_to_textnodes(block.replace("\n", " "))
    leaf_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
    parent_node = ParentNode("p", leaf_nodes)

    return parent_node


def markdown_to_html_node(markdown: str) -> ParentNode:

    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for block in blocks:
        html_nodes.append(block_to_html_node(block.strip()))

    return ParentNode("div", html_nodes)


