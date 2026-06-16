import unittest
from src.utils.textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text nodes", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("A text node", TextType.BOLD)
        self.assertIsNone(node.url)

    def test_url(self):
        node = TextNode("This is a text nodes", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node.text_type, node2.text_type)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_to_html_with_unkown_type(self):
        node = TextNode("This is a text node", "blue")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_every_type_to_html(self):
        cases = [
            (TextNode("hello", TextType.TEXT), "hello"),
            (TextNode("hello", TextType.BOLD), "<b>hello</b>"),
            (TextNode("hello", TextType.ITALIC), "<i>hello</i>"),
            (TextNode("hello", TextType.CODE), "<code>hello</code>"),
            (
                TextNode("hello", TextType.LINK, "https://google.com"),
                '<a href="https://google.com">hello</a>',
            ),
            (
                TextNode("hello", TextType.IMAGE, "https://google.com"),
                '<img src="https://google.com" alt="hello"></img>',
            ),
        ]

        for text_node, res in cases:
            self.assertEqual(text_node_to_html_node(text_node).to_html(), res)

    def test_empty_delimeter(self):
        node = TextNode("****", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(result, [TextNode("", TextType.BOLD)])

    def test_split_multiple_inline_elements(self):
        node = TextNode("This is **bold** and **strong**", TextType.TEXT)

        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("strong", TextType.BOLD),
            ],
        )

    def test_adjacent_delimiters(self):
        node = TextNode("**a****b**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            result,
            [
                TextNode("a", TextType.BOLD),
                TextNode("b", TextType.BOLD),
            ],
        )

    def test_invalid_split_node_delimiter(self):
        node = TextNode(
            "This is text with a **bolded phrase in the middle", TextType.TEXT
        )
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )

        self.assertListEqual(
            matches,
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")] )
    
    def test_extract_markdown_without_image_markers(self):
        matches = extract_markdown_images(
            "This is text with a no image"
        )
        self.assertListEqual(matches , [])
    
    def test_extract_markdown_without_links_markers(self):
        matches = extract_markdown_links(
            "This is text with a no link"
        )
        self.assertListEqual(matches , [])
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_link(self):
        node = TextNode(
            "This is text with an [first link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("first link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_text_containing_both_link_and_images(self):
        node = TextNode("![img](url)[link](url2)", TextType.TEXT)

        self.assertListEqual(
            split_nodes_image([node]),
            [ TextNode("img" , TextType.IMAGE , "url"), TextNode("[link](url2)", TextType.TEXT)] 
        )
        self.assertListEqual(
            split_nodes_link([node]),
            [ TextNode("![img](url)", TextType.TEXT) , TextNode("link" , TextType.LINK , "url2")] 
        )

    def test_text_to_textnode(self):

        text = "This is **text** with an _italic_ word and another bold **text** and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(
            text_to_textnodes(text),
            [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and another bold ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" and a " ,TextType.TEXT ),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )
        
if __name__ == "__main__":
    unittest.main()
