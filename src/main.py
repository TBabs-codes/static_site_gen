import os
import shutil

shutil.rmtree("./public") #deletes entire public directory.

os.mkdir("./public") #creates public directory.

def copyfiles(src_path, dst_path): #copyfiles function copies files from src_path directory into dst_path directory preserving the orginal file tree.

    static_file_tree = os.listdir(f"{src_path}")

    for obj in static_file_tree:
        if os.path.isfile(f"{src_path}/{obj}"):
            shutil.copy(f"{src_path}/{obj}", f"{dst_path}")
        else:
            os.mkdir(f"{dst_path}/{obj}")
            copyfiles(f"{src_path}/{obj}", f"{dst_path}/{obj}")

copyfiles("./static", "./public") #This code is readable. No comment.