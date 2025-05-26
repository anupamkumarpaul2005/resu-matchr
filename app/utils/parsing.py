import fitz
from llama_parse import LlamaParse
import os
from dotenv import load_dotenv

load_dotenv()

def parse_with_PyMuPDF(file_path):
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip()
    except Exception as e:
        print(f"[fitz] Error: {e}")
        return ""

def parse_with_llamaparse(pdf_path):
    parser = LlamaParse(
        api_key=os.getenv("LLAMA_CLOUD_API_KEY"),
        result_type="markdown",
        verbose=False
    )

    try:
        documents = parser.load_data(pdf_path)
        if not documents:
            raise ValueError("No documents returned.")

        resume_text = documents[0].text.strip()
        return resume_text

    except Exception as e:
        print(f"[LlamaParse] Error: {e}")
        return None

def extract_text_from_pdf(file_path):
    print("Trying LlamaParse first...")
    text = parse_with_llamaparse(file_path)

    if text:
        print("LlamaParse extraction successful.")
        return text
    else:
        print("Falling back to fitz extraction...")
        return parse_with_PyMuPDF(file_path)
