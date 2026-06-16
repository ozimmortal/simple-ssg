import os, shutil, sys
from utils.helper_functions import extract_title
from utils.blocknode import *

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():

    args = sys.argv
    basepath = args[1] if len(args) >= 2 else "/"

    static_src_path, static_des_path = os.path.join(
        ROOT_DIR, "src/static"
    ), os.path.join(ROOT_DIR, "docs")
    clean_and_copy_all_contents(
        static_src_path, static_des_path
    )  # copy the static files

    md_src_path, md_des_path, template_path = (
        os.path.join(ROOT_DIR, "content"),
        os.path.join(ROOT_DIR, "docs"),
        os.path.join(ROOT_DIR, "src/template.html"),
    )
    
   

    generate_pages_recursive(md_src_path, template_path, md_des_path , basepath)


def clean_destination_directory(path):

    if not os.path.exists(path):
        return

    for item in os.listdir(path):
        item_path = os.path.join(path, item)

        if os.path.isfile(item_path):
            os.remove(item_path)
        else:
            clean_destination_directory(item_path)

    os.rmdir(path)


def copy_all_contents(src, destination):

    if not os.path.exists(src) or not os.path.exists(destination):
        return

    for item in os.listdir(src):

        item_path = os.path.join(src, item)
        des_path = os.path.join(destination, item)

        if os.path.isfile(item_path):
            shutil.copy(item_path, des_path)
        else:
            os.mkdir(des_path)
            copy_all_contents(item_path, des_path)


def clean_and_copy_all_contents(src, destination):
    clean_destination_directory(destination)
    os.mkdir(destination)
    copy_all_contents(src, destination)


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    title, content = extract_title(markdown), markdown_to_html_node(markdown).to_html()
    html_file = (
        template.replace("{{ Title }}", title)
        .replace("{{ Content }}", content)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )

    directory_path, _ = os.path.split(dest_path)
    os.makedirs(directory_path, exist_ok=True)

    # print(dest_path)
    with open(dest_path, "w") as f:
        f.write(html_file)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path ,basepath):

    for item in os.listdir(dir_path_content):

        item_path = os.path.join(dir_path_content, item)
        des_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(item_path):
            des_path = des_path.replace(".md", ".html")
            generate_page(
                from_path=item_path, template_path=template_path, dest_path=des_path, basepath=basepath
            )
        else:
            generate_pages_recursive(item_path, template_path, des_path , basepath)


if __name__ == "__main__":
    main()
