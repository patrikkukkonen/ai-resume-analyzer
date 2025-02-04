import pdfplumber


# Improved version with parsing a pdf file with pdfplumber
# Open pdf
def extract_pdf(resume_name):
    pdf = pdfplumber.open(resume_name)
    page = pdf.pages[0]
    # Extract text
    text = page.extract_text()
    print(text)

    # Extract to tables
    # tables = page.extract_table()
    # for table in tables:
    #    print(table)

    # Extract images

    # Divide to sections
    # sections = re.split(r'\n(?=[A-Z][a-z]+:)', text)
    # print("SECTiONS: ", sections)

    return text
