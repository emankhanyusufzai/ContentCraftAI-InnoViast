# utils/exporters.py
# ContentCraft AI - Export helpers (PDF generation)

from fpdf import FPDF
from fpdf.enums import XPos, YPos


def _sanitize_line(line: str, max_word_len: int = 90) -> str:
    """
    Breaks up any single 'word' that's too long to fit on a line
    (e.g. a long URL with no spaces), which is what causes fpdf2's
    'Not enough horizontal space to render a single character' error.
    """
    words = []
    for word in line.split(" "):
        if len(word) > max_word_len:
            chunks = [word[i:i + max_word_len] for i in range(0, len(word), max_word_len)]
            words.append(" ".join(chunks))
        else:
            words.append(word)
    return " ".join(words)


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
    pdf.multi_cell(0, 10, _sanitize_line(safe_title), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    # Body
    pdf.set_font("Helvetica", size=12)
    safe_content = content.encode("latin-1", "replace").decode("latin-1")

    for line in safe_content.split("\n"):
        stripped = line.strip()
        if stripped == "":
            # Blank line: fpdf2's multi_cell() raises FPDFException on an
            # empty string, so use a plain line-break here instead.
            pdf.ln(6)
        else:
            # Explicitly forcing the cursor back to the left margin on the
            # next line after every call — without this, fpdf2 sometimes
            # leaves the cursor at the right edge of the page, which then
            # causes 'Not enough horizontal space' on the following line.
            pdf.multi_cell(0, 8, _sanitize_line(stripped), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    output = pdf.output()
    return bytes(output)