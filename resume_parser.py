import spacy
import re
import pdfplumber


# Improved version with parsing a pdf file with pdfplumber
# Open pdf
def extract_pdf(resume_name):
    pdf = pdfplumber.open(resume_name)
    page = pdf.pages[0]
    # Extract text
    text = page.extract_text()
    #print(text)

    # Extract to tables
    #tables = page.extract_table()
    #for table in tables:
    #    print(table)

    # Extract images

    return text


# Load spaCy model (english)
nlp = spacy.load("en_core_web_sm")


def extract_email(text):
    """Extract email addresses using regex."""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails


def extract_entities(text):
    """Extract entities from text using spaCy."""
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities


# Process sample resume text
def parse_resume(text):
    """Extract useful resume information from the text."""
    emails = extract_email(text)
    entities = extract_entities(text)

    # Filter entities by type (if needed)
    names = [ent[0] for ent in entities if ent[1] == "PERSON"]
    dates = [ent[0] for ent in entities if ent[1] == "DATE"]
    organizations = [ent[0] for ent in entities if ent[1] == "ORG"]

    # Extract entities (names, email, details etc.
    resume_info = {
        "emails": emails,
        "names": names,
        "dates": dates,
        "organizations": organizations,
        "all_entities": entities,
    }

    return resume_info


if __name__ == "__main__":
    # Example resume text (you can replace this with actual file input later)
    sample_text = """
    John Doe
    Email: john.doe@example.com
    Experience: Worked at OpenAI from January 2020 to March 2023.
    Education: B.Sc. in Computer Science from MIT.
    """

    #info = parse_resume(sample_text)
    print("Extracted Resume Information:")
    #for key, value in info.items():
    #    print(f"{key.capitalize()}: {value}")

    info = parse_resume(extract_pdf("resume.pdf"))
    for key, value in info.items():
        print(f"{key.capitalize()}: {value}")






