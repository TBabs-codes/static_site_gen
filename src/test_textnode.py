import unittest
import re

from textnode import (
    TextNode,
    text_node_to_html_node,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)
from textnode_functions import split_nodes_delimiter, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_textnodes



class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", "italic")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_eq3(self):
        node = TextNode("This is a text", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("Text goes here", "italic", "www.coal.com")
        node2 = TextNode("Text goes here", "italic", "www.coal.com")
        self.assertEqual(node.__repr__(), node2.__repr__())

    def test_repr2(self):
        node = TextNode("Text goes here", "italic",)
        node2 = TextNode("Text goes here", "italic",)
        self.assertEqual(node.__repr__(), node2.__repr__())
    
    def test_repr3(self):
        node = TextNode("Text goes here", "italic", "www.coal.com")
        node2 = TextNode("Text goes here", "italic",)
        self.assertEqual(node.__repr__(), 'TextNode(Text goes here, italic, www.coal.com)')

    def test_repr4(self):
        node = TextNode("Text goes here", "italic")
        node2 = TextNode("Text goes here", "italic",)
        self.assertEqual(node.__repr__(), 'TextNode(Text goes here, italic, None)')

    def test_textNode_to_html(self):
        node = TextNode("Super sick text", "italic")
        htmlnode = text_node_to_html_node(node)
        self.assertEqual(htmlnode.to_html(), '<i>Super sick text</i>')
    
class TestSplit_Nodes_Delimitter(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node. Only **this is bold**, this is not", "text")
        node2 = TextNode("**Just** some **bold**", "text")
        self.assertEqual(split_nodes_delimiter([node, node2], "**", "bold"), [TextNode("This is a text node. Only ", "text", None), 
                                                                                TextNode("this is bold", "bold", None), 
                                                                                TextNode(", this is not", "text", None), 
                                                                                TextNode("Just", "bold", None), 
                                                                                TextNode(" some ", "text", None), 
                                                                                TextNode("bold", "bold", None)])
        

class Test_Extract_Markdown_Images_and_Links(unittest.TestCase):
    def test_extract_markdown_images_2images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_split_nodes_images1(self): #test with one node.
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        old_node = TextNode(text, "text")
        new_node_list = [TextNode("This is text with a ", "text", None), TextNode("rick roll", "image", "https://i.imgur.com/aKaOqIh.gif"), TextNode(" and ", "text", None), TextNode("obi wan", "image", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(split_nodes_image([old_node]), new_node_list)

    def test_split_nodes_images2(self): #test with two nodes and additional text at the end of the string after image.
        text1 = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        text2 = "This is text with a ![roll](https://i.imgur.com/aKaOqIh.gif) and ![wan](https://i.imgur.com/fJRm4Vk.gif) litte extra something"
        old_node1 = TextNode(text1, "text")
        old_node2 = TextNode(text2, "text")
        new_node_list = [TextNode("This is text with a ", "text", None), 
                         TextNode("rick roll", "image", "https://i.imgur.com/aKaOqIh.gif"), 
                         TextNode(" and ", "text", None), 
                         TextNode("obi wan", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),
                         TextNode("This is text with a ", "text", None), 
                         TextNode("roll", "image", "https://i.imgur.com/aKaOqIh.gif"), 
                         TextNode(" and ", "text", None), 
                         TextNode("wan", "image", "https://i.imgur.com/fJRm4Vk.gif"),
                         TextNode(" litte extra something", "text", None)]
        self.assertEqual(split_nodes_image([old_node1, old_node2]), new_node_list)

    def test_split_nodes_links1(self):
        node1 = TextNode("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", "text")
        new_node_list = [TextNode("This is text with a ", "text", None), 
                         TextNode("rick roll", "link", "https://i.imgur.com/aKaOqIh.gif"), 
                         TextNode(" and ", "text", None), 
                         TextNode("obi wan", "link", "https://i.imgur.com/fJRm4Vk.jpeg"),]
        self.assertListEqual(new_node_list, split_nodes_link([node1])) 

class Test_Text_to_TextNodes(unittest.TestCase):
    def test_longstring_from_bootdev(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_nodes = [TextNode("This is ", text_type_text),
                            TextNode("text", text_type_bold),
                            TextNode(" with an ", text_type_text),
                            TextNode("italic", text_type_italic),
                            TextNode(" word and a ", text_type_text),
                            TextNode("code block", text_type_code),
                            TextNode(" and an ", text_type_text),
                            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
                            TextNode(" and a ", text_type_text),
                            TextNode("link", text_type_link, "https://boot.dev"),]
        
        self.assertEqual(text_to_textnodes(text), expected_nodes)


if __name__ == "__main__":
    unittest.main()