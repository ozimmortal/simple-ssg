import unittest
from src.utils.blocknode import *


class TestBlockNode(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_strips_leading_trailing_whitespace(self):
        md = "   \n\nHello\n\nWorld\n\n   "
        self.assertEqual(markdown_to_blocks(md), ["Hello", "World"])

    def test_multiple_blank_lines_between_blocks(self):
        # This is the bug — passes only after the fix
        md = "Block one\n\n\n\nBlock two"
        self.assertEqual(markdown_to_blocks(md), ["Block one", "Block two"])

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_only_whitespace(self):
        self.assertEqual(markdown_to_blocks("   \n\n   "), [])

    def test_block_to_block_type(self):

        cases = [
            ("This is **bolded** paragraph", BlockType.PARAGRAPH),
            ("# This is a Heading h1", BlockType.HEADING),
            ("## This is a Heading h2", BlockType.HEADING),
            ("###### This is a Heading h6", BlockType.HEADING),
            (
                """```
                def hello():
                    print("hello")
                ```""",
                BlockType.CODE,
            ),
            (
                "> This is a quote\n> another quote line",
                BlockType.QUOTE,
            ),
            (
                "- first item\n- second item\n- third item",
                BlockType.UNORDERED_LIST,
            ),
            (
                "- first item\n- second item",
                BlockType.UNORDERED_LIST,
            ),
            (
                "1. first\n2. second\n3. third",
                BlockType.ORDERED_LIST,
            ),
            (
                "1. first\n3. second",
                BlockType.PARAGRAPH,
            ),
            (
                "1. first\n2. second\n4. third",
                BlockType.PARAGRAPH,
            ),
        ]

        for block, expected in cases:
            self.assertEqual(block_to_block_type(block), expected)
    
    def test_quote_type(self):
        md = """
> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
"""
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)

    def test_heading_invalid(self):
        self.assertEqual(
            block_to_block_type("####### too many hashes"), BlockType.PARAGRAPH
        )

    def test_quote_invalid(self):
        self.assertEqual(
            block_to_block_type("""> line 1
    not quoted"""),
            BlockType.PARAGRAPH,
        )

    def test_code_invalid(self):
        self.assertEqual(block_to_block_type("```python"), BlockType.PARAGRAPH)
    
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_all_nodes(self):
        md = """
# Heading One with **bold** and _italic_ .

## Heading Two

```
def hello():
print("hello")
```

> This is a quote
> with two lines

- first item
- second item
- third item

1. first ordered
2. second ordered
3. third ordered

This is a **bolded** paragraph with _italic_ and `code` text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        
        
        # heading one with bold and italic
        self.assertIn("<h1>Heading One with <b>bold</b> and <i>italic</i> .</h1>" , html)

        # heading two
        self.assertIn("<h2>Heading Two</h2>", html)

        # code
        self.assertIn("<pre><code>", html)
        self.assertIn("def hello():", html)

        # quote
        self.assertIn("<blockquote>", html)
        self.assertIn("This is a quote", html)

        # unordered list
        self.assertIn("<ul>", html)
        self.assertIn("<li>first item</li>", html)

        # ordered list
        self.assertIn("<ol>", html)
        self.assertIn("<li>first ordered</li>", html)

        # paragraph with inline markdown
        self.assertIn("<p>", html)
        self.assertIn("<b>bolded</b>", html)
        self.assertIn("<i>italic</i>", html)
        self.assertIn("<code>code</code>", html)
