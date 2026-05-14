import fitz
from docx import Document


def extract_text_from_md_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
