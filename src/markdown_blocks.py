import re

from htmlnode import LeafNode, ParentNode

from textnode import TextNode, text_node_to_html_node
from textnode_functions import text_to_textnodes

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

def markdown_to_blocks(markdown): #Takes raw markdown and break it into blocks.
    
    return list(map(lambda x: x.strip("\n"), filter(lambda x: x.strip(), re.split(r'\n\s*\n\s*', markdown))))

def block_to_block_type(block): #returns the block type

    if block[0] == "#":
        return "heading"
    
    if block[:3] == "```" and block[-3:] == "```":
        return "code"
    
    if block[0] == ">":
        lines = block.split("\n")

        for line in lines:
            if line[0] != ">":
                return "paragraph"
            
        return "quote"

    if block[:2] == "* " or block[:2] == "- ":
        lines = block.split("\n")

        for line in lines:
            if line[:2] != "* " and line[:2] != "- ":
                return "paragraph"
            
        return "unordered_list"
    
    if block[:3] == "1. ":
        lines = block.split("\n")
        i = 1
        for line in lines:
            if line[:3] != f"{i}. ":
                return "paragraph"
            i+=1
            
        return "ordered_list"
    

    return "paragraph"


def heading_block_to_HTLMNode(block):
    
    value = block.strip("#")[1:]
    text_nodes = text_to_textnodes(value)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))

    heading_size = len(block) - len(block.lstrip("#"))

    return ParentNode(f"h{heading_size}", html_nodes, None)

def paragraph_block_to_HTMLNode(block):
    text_nodes = text_to_textnodes(block)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))

    return ParentNode("p", html_nodes)

def code_block_to_HTMLNode(block):
    code_block_node = LeafNode("code", block)
    return ParentNode("pre", [code_block_node])

def quote_block_to_HTMLNode(block):
    lines = list(map(lambda x: x[2:], block.split("\n")))
    text_nodes = []

    for i, line in enumerate(lines):
        if i > 0:
            text_nodes.extend(text_to_textnodes(" " + line))
        else:
            text_nodes.extend(text_to_textnodes(line))
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))

    return ParentNode("blockquote", html_nodes)


def ordered_list_block_to_HTMLNode(block):
    lines = list(map(lambda x: x[3:], block.split("\n")))
    html_nodes = []

    for line in lines:
        text_nodes = text_to_textnodes(line)
        line_html_nodes = []
        for node in text_nodes:
            line_html_nodes.append(text_node_to_html_node(node))
        html_nodes.append(ParentNode("li", line_html_nodes))
    

    return ParentNode("ol", html_nodes)

def unordered_list_block_to_HTMLNode(block):
    lines = list(map(lambda x: x[2:], block.split("\n")))
    html_nodes = []

    for line in lines:
        text_nodes = text_to_textnodes(line)
        line_html_nodes = []
        for node in text_nodes:
            line_html_nodes.append(text_node_to_html_node(node))
        html_nodes.append(ParentNode("li", line_html_nodes))
    

    return ParentNode("ul", html_nodes)




def markdown_to_html_node(markdown): #Converts a full markdown document into a single HTMLNode.
    blocks = markdown_to_blocks(markdown)
    parentNodes = []

    for block in blocks:
        type = block_to_block_type(block)

        match type:
            case "heading":
                parentNodes.append(heading_block_to_HTLMNode(block))
            case "paragraph":
                parentNodes.append(paragraph_block_to_HTMLNode(block))
            case "code":
                parentNodes.append(code_block_to_HTMLNode(block))
            case "quote":
                parentNodes.append(quote_block_to_HTMLNode(block))
            case "ordered_list":
                parentNodes.append(ordered_list_block_to_HTMLNode(block))
            case "unordered_list":
                parentNodes.append(unordered_list_block_to_HTMLNode(block))
            case _:
                raise ValueError("Block type not recognized.")
            
        
    return ParentNode("div", parentNodes, None)

