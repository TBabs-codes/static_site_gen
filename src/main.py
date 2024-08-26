import os
import shutil

from markdown_blocks import markdown_to_html_node
from htmlnode import ParentNode

def copyfiles(src_path, dst_path): #copyfiles function copies files from src_path directory into dst_path directory preserving the orginal file tree.

    static_file_tree = os.listdir(f"{src_path}")

    for obj in static_file_tree:
        if os.path.isfile(f"{src_path}/{obj}"):
            shutil.copy(f"{src_path}/{obj}", f"{dst_path}")
        else:
            os.mkdir(f"{dst_path}/{obj}")
            copyfiles(f"{src_path}/{obj}", f"{dst_path}/{obj}")

def extract_title(markdown):
    words = markdown.split(" ")
    for i, word in enumerate(words):
        if word == "#":
            return words[i+1]
    
    raise Exception("No h1 header found.")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    markdown = ""
    template = ""
    with open(f"{from_path}", 'r') as f:
        markdown = f.read()
        
    with open(f"{template_path}", 'r') as f:
        template = f.read()

    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    
    with open(f"{dest_path}", 'w') as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    
shutil.rmtree("./public") #deletes entire public directory.

os.mkdir("./public") #creates public directory.

print(os.listdir())

copyfiles("./static", "./public") #This code is readable. No comment.

generate_page("./src/content/index.md","./src/template.html","./public/index.html")
generate_page("./src/content/majesty/index.md","./src/template.html","./public/majesty/index.html")