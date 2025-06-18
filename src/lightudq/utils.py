import os

import pymupdf


def read_markdown_to_text(file_path: str) -> str:
    with open(file_path, encoding="utf-8") as f:
        return f.read()


def read_pdf_to_text(file_path: str) -> str:
    doc = pymupdf.open(file_path)
    text = ""
    for page in doc:  # iterate the document pages
        text += page.get_text()  # get plain text (is in UTF-8)
    return text


def read_document(file_path: str) -> str:
    """Read document content based on file extension"""
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension == ".md":
        return read_markdown_to_text(file_path)
    elif file_extension == ".txt":
        with open(file_path) as file:
            return file.read()
    elif file_extension == ".pdf":
        return read_pdf_to_text(file_path)
    else:
        print(f"Unsupported file format: {file_extension}")
        return ""
