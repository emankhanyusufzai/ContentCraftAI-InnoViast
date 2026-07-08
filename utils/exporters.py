# utils/exporters.py
# ContentCraft AI - Export helpers (PDF generation)

from fpdf import FPDF


def generate_pdf_bytes(title: str, content: str) -> bytes:
    """
    Converts generated content into a simple, clean PDF and returns raw bytes.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 16)
    safe_title = title.encode("latin-1", "replace").decode("latin-1")
    pdf.multi_cell(0, 10, safe_title)
    pdf.ln(4)

    # Body
    pdf.set_font("Helvetica", size=12)
    safe_content = content.encode("latin-1", "replace").decode("latin-1")
    for line in safe_content.split("\n"):
        pdf.multi_cell(0, 8, line)

    output = pdf.output()
    return bytes(output)
