import pdfplumber

import pdfminer # Try pdf extraction with pdfminer.six


# PDF Extraction Function
# Parsing a pdf file with pdfplumber
def extract_text_from_pdf(pdf_path):
    """Extract text from pdf file using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Loop trough each page incase the pdf has multiple pages
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print("Error reading the PDF file: ", e)
    print(text)  # For debugging
    return text

    # page = pdf.pages[0]
    # Extract text
    # text = page.extract_text()

    # Extract to tables
    # tables = page.extract_table()
    # for table in tables:
    #    print(table)

    # Extract images

    # Divide to sections
    # sections = re.split(r'\n(?=[A-Z][a-z]+:)', text)
    # print("SECTiONS: ", sections)

    # return text
