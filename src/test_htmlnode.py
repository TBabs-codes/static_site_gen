import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        prop = dict()
        prop["href"] = "https://www.google.com"
        prop["target"] = "_blank"
        node = HTMLNode("<p>", "Some dope text in a paragraph", ["stuff","andthings"], prop)
        
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")

    def test_repr(self):
        node = HTMLNode("<h>", "This is a header",)
        self.assertEqual(node.__repr__(), "HTMLNode():\ntag: <h>\nvalue: This is a header\nchildren: None\nprops: None")
        
class TestLeafNode(unittest.TestCase):
    def test_to_html(self):

        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")


class TestParentNode(unittest.TestCase):
    def test_to_html(self): #only LeafNodes in Parent

        node = ParentNode("p", [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
        ],)

        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html2(self):

        node = ParentNode("p", [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
        ParentNode("p",
        [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
        ],)
        ],)

        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p>")

    def test_to_html3(self):

        node = ParentNode("p", [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
        ParentNode("p",
        [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
        ParentNode("p",
        [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
        ],)
        ],)
        ],)

        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text<p><b>Bold text</b>Normal text<i>italic text</i>Normal text<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p></p>")

    def test_to_html4(self):

        node = ParentNode("p", [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
        ParentNode("p",
        [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
        ParentNode("p",[],)
        ],)
        ],)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "Value Error3: No children found in ParentNode.")

        
if __name__ == "__main__":
    unittest.main()


ParentNode("p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],)