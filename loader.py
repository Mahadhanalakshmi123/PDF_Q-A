import io
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from pdf2image import convert_from_bytes
import easyocr

reader = easyocr.Reader(['en'], gpu=False)

def load_pdf_text(pdf_bytes: bytes) -> str:
    reader_pdf = PdfReader(io.BytesIO(pdf_bytes))
    text = ""

    for page in reader_pdf.pages:
        page_text = page.extract_text()
        if page_text and page_text.strip():
            text += page_text + "\n"

    if not text.strip():
        images = convert_from_bytes(pdf_bytes)
        for img in images:
            ocr_lines = reader.readtext(img, detail=0, paragraph=True)
            text += "\n".join(ocr_lines) + "\n"

    return text

def chunk_text(text: str, chunk_size=500, overlap=50) -> list[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks
