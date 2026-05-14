import fitz
from docx import Document


def extract_text_from_md_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def extract_text_from_pdf(file_path):
    document = fitz.open(file_path)
    text = ""
    for page in document:
        text = text + page.get_text()
    return text


def extract_text_from_docx(file_path):
    document = Document(file_path)
    text = ""
    for paragraph in document.paragraphs:
        text = text + paragraph.text + "\n"
    return text


def extract_text(file_path, extension):
    if extension == ".txt" or extension == ".md":
        return extract_text_from_md_txt(file_path)
    elif extension == ".pdf":
        return extract_text_from_pdf(file_path)
    elif extension == ".docx":
        return extract_text_from_docx(file_path)
    else:
        raise Exception("Unsupported file type")
