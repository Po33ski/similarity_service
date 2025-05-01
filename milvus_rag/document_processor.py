import fitz  # PyMuPDF
import json
import os

def process_pdf(pdf_path: str, output_json: str):
    doc = fitz.open(pdf_path)
    pages = []
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text().replace('\n', ' ').strip()
        if text:  # Skip empty pages
            pages.append({
                "page_num": page_num + 1,
                "text": text
            })
    
    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    with open(output_json, 'w') as f:
        json.dump(pages, f, indent=2, ensure_ascii=False)