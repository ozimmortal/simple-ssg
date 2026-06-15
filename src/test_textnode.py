import unittest
from textnode import TextNode, TextType , text_node_to_html_node

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
        node = TextNode("A text node" , TextType.BOLD)
        self.assertIsNone(node.url)
    def test_url(self):
        node = TextNode("This is a text nodes", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node.text_type , node2.text_type)
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
        (TextNode("hello", TextType.TEXT),  "hello"),
        (TextNode("hello", TextType.BOLD),   "<b>hello</b>"),
        (TextNode("hello", TextType.ITALIC), "<i>hello</i>"),
        (TextNode("hello", TextType.CODE),   "<code>hello</code>"),
        (TextNode("hello", TextType.LINK, "https://google.com"),  '<a href="https://google.com">hello</a>'),
        (TextNode("hello", TextType.IMAGE, "https://google.com"), '<img src="https://google.com" alt="hello"></img>'),
        ]

        for text_node , res in cases:
            self.assertEqual(text_node_to_html_node(text_node).to_html() , res)
            

        



if __name__ == "__main__":
    unittest.main()