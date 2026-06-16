
#  extract a the title from the md file
def extract_title(markdown: str) -> str:
    markdown = markdown.strip()

    if markdown.find("# ") != 0:
        raise Exception("There is no title to extract.")

    _ , title = markdown.split("\n")[0].split(" ", 1)
    return title
