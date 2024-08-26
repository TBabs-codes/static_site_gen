import os
import shutil

from markdown_blocks import markdown_to_html_node
from htmlnode import ParentNode
from content_generation import copyfiles, generate_pages_recursive


shutil.rmtree("./public") #deletes entire public directory.

os.mkdir("./public") #creates public directory.

print(os.listdir())

copyfiles("./static", "./public") #This code is readable. No comment.

generate_pages_recursive("./src/content","./src/template.html","./public")
