import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io

def extract_text_from_pdf(uploaded_file):
    """Extract text from uploaded PDF file."""
    text = ""
    try:
        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        for page_num in range(len(doc)):
            page = doc[page_num]
            page_text = page.get_text()

            # If page has no text (scanned/image PDF), use OCR
            if len(page_text.strip()) < 50:
                pix = page.get_pixmap(dpi=200)
                img_bytes = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_bytes))
                page_text = pytesseract.image_to_string(img)

            text += f"\n--- Page {page_num + 1} ---\n{page_text}"

        doc.close()
        return text.strip()

    except Exception as e:
        return f"Error extracting text: {str(e)}"


def extract_text_from_txt(uploaded_file):
    """Extract text from plain text file."""
    try:
        return uploaded_file.read().decode("utf-8")
    except Exception as e:
        return f"Error reading file: {str(e)}"
