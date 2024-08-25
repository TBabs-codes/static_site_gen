import re

from textnode import TextNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

delimiter_types = {"bold": '**', "italic": '*', "code": '`'}

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node_list = []

    for node in old_nodes:
        if node.text_type != "text":
            new_node_list.append(node)
            continue
        temp_list = node.text.split(f'{delimiter}')
        if len(temp_list) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        i = 1
        for words in temp_list:
            if i==1 and words != "":
                new_node_list.append(TextNode(words, text_type_text))
            elif i == -1 and words != "":
                new_node_list.append(TextNode(words, text_type))

            i = i*-1

    return new_node_list

def extract_markdown_images(text):

    alt_text_matches = re.findall(r"\!\[(.*?)\]\(", text)
    url_matches = re.findall(r"\]\((http.*?)\)", text)
    images = []
    if len(alt_text_matches) == len(url_matches):
        for i, match in enumerate(alt_text_matches):
            images.append((match, url_matches[i]))
    return images
    
    
def extract_markdown_links(text):
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    final_nodes = []
    for node in old_nodes:
        new_nodes = []
        images = extract_markdown_images(node.text) # should test when the text doesn't have an image.

        if len(images) != 0:
            remaining_text = node.text
            for i, image in enumerate(images):
                split_index = remaining_text.find(f"![{images[i][0]}]") #finds the start of the image's alt text
                image_end_index = remaining_text.find(f"{images[i][1]}") + len(images[i][1])+1
                new_nodes.extend([TextNode(remaining_text[:split_index], "text"),
                                TextNode(images[i][0], "image", images[i][1])
                                ])
                remaining_text = remaining_text[image_end_index:]

            final_nodes.extend(new_nodes)

            if remaining_text != "":
                final_nodes.append(TextNode(remaining_text, "text"))
        else:
            final_nodes.append(node)

    return final_nodes

def split_nodes_link(old_nodes):
    final_nodes = []
    for node in old_nodes:
        new_nodes = []
        images = extract_markdown_links(node.text) # should test when the text doesn't have an image.

        if len(images) != 0:
            remaining_text = node.text
            for i, image in enumerate(images):
                split_index = remaining_text.find(f"[{images[i][0]}]") #finds the start of the image's alt text
                image_end_index = remaining_text.find(f"{images[i][1]}") + len(images[i][1])+1
                new_nodes.extend([TextNode(remaining_text[:split_index], "text"),
                                TextNode(images[i][0], "link", images[i][1])
                                ])
                remaining_text = remaining_text[image_end_index:]

            final_nodes.extend(new_nodes)

            if remaining_text != "":
                final_nodes.append(TextNode(remaining_text, "text"))
        else:
            final_nodes.append(node)

    return final_nodes

def text_to_textnodes(text): #returns list of TextNodes of all types from string of text.
    nodes = [TextNode(text, "text")]
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    for text_type, delimiter in delimiter_types.items():
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)

    
    return nodes
