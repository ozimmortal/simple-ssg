import unittest
from src.utils.htmlnode import *


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        expected_attrs = [
            'href="https://www.google.com"',
            'target="_blank"',
        ]

        html_node = HTMLNode(props=props)
        result = html_node.props_to_html()

        for attr in expected_attrs:
            self.assertIn(attr, result)

    def test_attr_starts_with_whitespace(self):
        props = {"target": "_blank"}
        html_node = HTMLNode(props=props)
        results = html_node.props_to_html()
        self.assertTrue(results.startswith(" "))

    def node_eq(self):
        node1 = HTMLNode(tag="p", value="hello world")
        node2 = HTMLNode(tag="p", value="hello world")

        self.assertEqual(node1, node2)

    def test_leaf_to_html_p(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_with_no_tag(self):
        node = LeafNode(None, "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "Click me!")

    def test_leaf_with_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode(
                tag="a", value=None, props={"href": "https://www.google.com"}
            ).to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_parent_with_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode(
                tag="a", children=None , props={"href": "https://www.google.com"}
            ).to_html()
    
    def test_parent_with_no_tag(self):
        child_node = LeafNode("b", "child")
        with self.assertRaises(ValueError):
            ParentNode(
                None, children=[child_node], props={"href": "https://www.google.com"}
            ).to_html()

if __name__ == "__main__":
    unittest.main()